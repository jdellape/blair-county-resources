import streamlit as st
import json
import pandas as pd
from organization import Organization
from service import Service
from weekly_schedule import WeeklySchedule
from daily_schedule import DailySchedule, DailyMealSchedule
from google.cloud import firestore
from google.oauth2 import service_account

#Set global vars
tab1, tab2, tab3 = st.tabs(["Add New Organization", "Edit / Add Schedules to Existing Organization", "View Report"])

SERVICES_OPTIONS = []

DAYS_OF_WEEK = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

MEALS = ["Breakfast", "Lunch", "Dinner"]

SERVICES_ON_SCHEDULE = ['Food/Pantries','Food/Meals','Warming Center']

SERVICES_ON_SCHEDULE_KEY_STRING_DICT = {'Food/Pantries':'food_pantries_','Food/Meals':'food_meals_','Warming Center':'warming_center_'}

#Read in list of available services
with open('available_services.txt') as f:
    for line in f.readlines():
        SERVICES_OPTIONS.append(line.strip())

#Define functions
@st.cache_resource
def get_db_object():
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="streamlit-sources")
    return db

def get_editable_df_for_basic_schedule(service_key):
    is_available = [False for x in DAYS_OF_WEEK]
    open_times = ["" for x in DAYS_OF_WEEK]
    close_times = ["" for x in DAYS_OF_WEEK]
    df = pd.DataFrame(list(zip(DAYS_OF_WEEK, is_available, open_times, close_times)),
    columns =['day', 'available', 'beginning at', 'ending at'])
    return st.experimental_data_editor(df, key=service_key + '_weekly_schedule')   

def get_editable_df_for_meal_schedule(service_key):
    is_available = []
    days = []
    meals = []
    open_times = []
    close_times = []
    for day in DAYS_OF_WEEK:
        for meal in MEALS:
            is_available.append(False)
            days.append(day)
            meals.append(meal)
            open_times.append("")
            close_times.append("")
    df = pd.DataFrame(list(zip(days, meals, is_available, open_times, close_times)),
    columns =['day', 'meal', 'available', 'beginning at', 'ending at'])
    return st.experimental_data_editor(df, key=service_key + '_weekly_schedule')   

def get_service_list_intersection(db_doc_services_name_list):
    return set(SERVICES_OPTIONS).intersection(db_doc_services_name_list)

def get_service_names_from_db_doc(doc):
    return [service for service in list(doc['services'].keys())]      

def get_service_check_boxes_for_existing_agency(doc):
    service_list_to_return  = []
    #get list intersection
    found_services = get_service_names_from_db_doc(doc)
    for service in SERVICES_OPTIONS:
        #Check if it has a schedule
        #has_schedule_flag = service['has_schedule']
        if service in found_services:
            service_list_to_return.append(st.checkbox(label=service, value=True, key=service))
        else:
            service_list_to_return.append(st.checkbox(label=service, value=False, key=service))
    return service_list_to_return

def get_services_with_schedules(services_dict):
    #This returns a list of strings
    return [s for s in list(services_dict.keys()) if s in SERVICES_ON_SCHEDULE]

def get_schedule_entry_object_for_service(service_name):
    if service_name == "Food/Meals":
        return get_editable_df_for_meal_schedule(SERVICES_ON_SCHEDULE_KEY_STRING_DICT[service_name])
    else:
        return get_editable_df_for_basic_schedule(SERVICES_ON_SCHEDULE_KEY_STRING_DICT[service_name])
    
def get_ordered_df_column_list(service_name):
    if service_name == 'Food/Meals':
        return ['day','meal','available','beginning at','ending at']
    else:
        return ['day', 'available','beginning at','ending at']

#Make connection to firestore db
DB = get_db_object()

AGENCY_REF = DB.collection("agencies")
AGENCY_LIST = [doc.to_dict() for doc in AGENCY_REF.stream()]
AGENCY_NAMES = [agency['name'] for agency in AGENCY_LIST]

#Begin Add New Org Code
with tab1:
    st.header('Enter Organization Information')
    st.subheader('Required Fields')
    name = st.text_input('Name', key='org_name')
    st.write('Location')
    address_line_one = st.text_input('Address')
    city = st.text_input('City')
    zip_code = st.text_input('Zip Code')
    phone_num = st.text_input('Phone Number')

    #We Now have all the required fields. Create an organization object
    organization = Organization(name, address_line_one, city, zip_code, phone_num)

    st.subheader('Optional Fields')
    #Just set these fields even if blank
    contact_name = st.text_input('Name of Contact')
    organization.set_contact(contact_name)
    email = st.text_input('Email')
    organization.set_email(email)
    st.write("Schedule")
    hours_of_operation_df = get_editable_df_for_basic_schedule('hours_of_operation')
    organization.set_hours_of_operation(list(hours_of_operation_df.T.to_dict().values()))

    #Move onto services data entry
    st.header('Select Services Provided')
    for service in SERVICES_OPTIONS:
        service_checked = st.checkbox(service)
        #If box is checked for service, create service object and attach it to org object
        if service_checked:
            service_obj = Service(service)
            organization.add_service(service_obj)

    # Developer view of record for debugging
    # st.write('Developer Record Preview')
    # st.json(organization.__dict__, expanded=False)
    
    #Create ability to submit data to the firestore db collection
    if st.button('Submit New Agency'):
        #Create the new doc record in firestore
        doc_ref = DB.collection("agencies").document(name)
        try:
            doc_ref.set(organization.__dict__)
            st.success('Organization successfully added!', icon="✅")
        except Exception as e:
            st.error('An error has occurred', icon="🚨")
            st.exception(e)

#Begin Edit / Add Schedules to Existing Org Code
with tab2:
    agency_ref = DB.collection("agencies")
    agency_name_search = st.selectbox('Select an Organization to Update', options=[""] + AGENCY_NAMES)
    if agency_name_search != "":
        #Get the agency from db
        agency = [a for a in AGENCY_LIST if a['name'] == agency_name_search][0]
        #Allow for user input
        st.subheader('General Information')
        phone_num = st.text_input(label='Phone Number', value=agency['phone_num'], key='phone_num')
        address_line_one = st.text_input(label='Address', value=agency['address_line_one'], key='address_line_one')
        city = st.text_input(label='City', value=agency['city'], key='city')
        zip_code = st.text_input(label='Zip Code', value=agency['zip_code'], key='zip_code')
        contact_name = st.text_input(label='Contact Name', value=agency['contact_name'], key='contact_name')
        email = st.text_input(label='Email', value=agency['email'], key='email')
        hours_of_operation_schedule_for_input = None
        try:
            #Fetch from db if exists
            hours_of_operation_df_from_db = pd.DataFrame.from_dict(agency['hours_of_operation'])
            hours_of_operation_df_from_db = hours_of_operation_df_from_db[get_ordered_df_column_list('hours_of_operation')]
            st.write('Schedule Previously Uploaded to Database:')
            #Convert to editable dataframe
            hours_of_operation_schedule_for_input = st.experimental_data_editor(hours_of_operation_df_from_db, key='hours_of_operation_editable_df')
        except:
            #Assign a new schedule for entry if it doesn't exist currently in db
            hours_of_operation_schedule_for_input = get_editable_df_for_basic_schedule('hours_of_operation_edit_screen')
        
        #Compile organization object
        organization = Organization(agency_name_search, address_line_one, city, zip_code, phone_num)
        organization.set_contact(contact_name)
        organization.set_email(email)
        organization.set_hours_of_operation(list(hours_of_operation_schedule_for_input.T.to_dict().values()))

        #Begin handling services
        #Retrieve and display services with checkboxes
        st.subheader('Services Provided')
        for name, check_box in zip(SERVICES_OPTIONS, get_service_check_boxes_for_existing_agency(agency)):
            if check_box:
                service_obj = Service(name)
                #Handle schedules
                if name in SERVICES_ON_SCHEDULE:
                    st.write(f'Enter Schedule for {name}:')
                    schedule_for_input = None
                    #Get the editable df for schedule entry
                    try:
                        #Fetch from db if exists
                        schedule_df_from_db = pd.DataFrame.from_dict(agency['services'][name]['schedule'])
                        schedule_df_from_db = schedule_df_from_db[get_ordered_df_column_list(name)]
                        st.write('Schedule Previously Uploaded to Database:')
                        #Convert to editable dataframe
                        schedule_for_input = st.experimental_data_editor(schedule_df_from_db, key=name+'_editable_df')
                    except:
                        #Assign a new schedule for entry if it doesn't exist currently in db
                        schedule_for_input = get_schedule_entry_object_for_service(name)
                    #structure the data for document update in firestore
                    schedule_for_db = list(schedule_for_input.T.to_dict().values())
                    service_obj.set_schedule(schedule_for_db)
                    organization.add_service(service_obj)
                #If not on a schedule, simply add service object
                else:
                    organization.add_service(service_obj)

        # Developer view of record for debugging
        #Output previews of the json to be submitted
        # st.write('Developer Record Preview')
        # st.json(organization.__dict__, expanded=False)
        if st.button('Update Agency'):
            doc_ref = DB.collection("agencies").document(agency_name_search)
            try:
                doc_ref.set(organization.__dict__)
                st.success('Organization successfully updated!', icon="✅")
            except Exception as e:
                st.error('An error has occurred', icon="🚨")
                st.exception(e)

with tab3:
    #Radio button to either view all agencies or restrict by name or service
    st.subheader('Report View Mode')
    view_mode_selection = st.radio('View Mode', options=['All Organizations','Single Organization','Organizations Based on Services Provided'],
                                   horizontal=True, label_visibility='hidden')
    #Show all orgs by default
    if view_mode_selection == 'All Organizations':
        for agency in AGENCY_LIST:
            st.subheader(agency['name'])
            st.write(f"Phone #: ", agency['phone_num'])
            with st.expander("See More Information"):
                st.write(f"Address : {agency['address_line_one']}")
                st.write(f"City : {agency['city']}")
                st.write(f"Zip Code : {agency['zip_code']}")
                st.write(f"Contact Name : {agency['contact_name']}")
                st.write(f"Email : {agency['email']}")
                st.write('Schedule :')
                hours_of_operation_from_db = pd.DataFrame.from_dict(agency['hours_of_operation'])
                hours_of_operation_from_db = hours_of_operation_from_db[get_ordered_df_column_list('hours_of_operation_view')]
                st.write(hours_of_operation_from_db)
                st.subheader('Services')
                for service in agency['services']:
                    st.write(service)
                    if agency['services'][service]['has_schedule']:
                        schedule_df_from_db = pd.DataFrame.from_dict(agency['services'][service]['schedule'])
                        schedule_df_from_db = schedule_df_from_db[get_ordered_df_column_list(service)]
                        st.write(schedule_df_from_db)

    #filter the agency_list for only a single agency name selected by user
    if view_mode_selection == 'Single Organization':
        selected_agency = st.selectbox('Select an Agency to Update', options=[""] + AGENCY_NAMES, key='selected_agency_view_report')
        if selected_agency != "":
            #Get the agency from db
            agency = [a for a in AGENCY_LIST if a['name'] == selected_agency][0]
            st.subheader(agency['name'])
            st.write(f"Phone #: ", agency['phone_num'])
            with st.expander("See More Information"):
                st.write(f"Address : {agency['address_line_one']}")
                st.write(f"City : {agency['city']}")
                st.write(f"Zip Code : {agency['zip_code']}")
                st.write(f"Contact Name : {agency['contact_name']}")
                st.write(f"Email : {agency['email']}")
                st.write('Schedule :')
                hours_of_operation_from_db = pd.DataFrame.from_dict(agency['hours_of_operation'])
                hours_of_operation_from_db = hours_of_operation_from_db[get_ordered_df_column_list('hours_of_operation_view')]
                st.write(hours_of_operation_from_db)
                st.subheader('Services')
                for service in agency['services']:
                    st.write(service)
                    if agency['services'][service]['has_schedule']:
                        schedule_df_from_db = pd.DataFrame.from_dict(agency['services'][service]['schedule'])
                        schedule_df_from_db = schedule_df_from_db[get_ordered_df_column_list(service)]
                        st.write(schedule_df_from_db)

    #filter the agency_list for only agencies which provide a particular service
    if view_mode_selection == 'Organizations Based on Services Provided':
        selected_service = st.selectbox('Select Service of Interest', options=[""] + SERVICES_OPTIONS, key='selected_service_view_report')
        if selected_service != "":
            #Get the agency from db
            agencies_with_selected_service_list = []
            for a in AGENCY_LIST:
                try:
                    service = a['services'][selected_service]
                    agencies_with_selected_service_list.append(a)
                except:
                    pass
            for agency in agencies_with_selected_service_list:
                st.subheader(agency['name'])
                st.write(f"Phone #: ", agency['phone_num'])
                with st.expander("See More Information"):
                    st.write(f"Address : {agency['address_line_one']}")
                    st.write(f"City : {agency['city']}")
                    st.write(f"Zip Code : {agency['zip_code']}")
                    st.write(f"Contact Name : {agency['contact_name']}")
                    st.write(f"Email : {agency['email']}")
                    st.write('Schedule :')
                    hours_of_operation_from_db = pd.DataFrame.from_dict(agency['hours_of_operation'])
                    hours_of_operation_from_db = hours_of_operation_from_db[get_ordered_df_column_list('hours_of_operation_view')]
                    st.write(hours_of_operation_from_db)
                    st.subheader('Services')
                    for service in agency['services']:
                        st.write(service)
                        if agency['services'][service]['has_schedule']:
                            schedule_df_from_db = pd.DataFrame.from_dict(agency['services'][service]['schedule'])
                            schedule_df_from_db = schedule_df_from_db[get_ordered_df_column_list(service)]
                            st.write(schedule_df_from_db)
