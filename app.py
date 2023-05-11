import streamlit as st
import json
import pandas as pd
from organization import Organization
from service import Service
from weekly_schedule import WeeklySchedule
from daily_schedule import DailySchedule, DailyMealSchedule

tab1, tab2 = st.tabs(["Enter New Organization", "Report on Existing Organizations"])

SERVICES_OPTIONS = []

DAYS_OF_WEEK = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

MEALS = ["Breakfast", "Lunch", "Dinner"]

SERVICES_ON_SCHEDULE = ['Food/Pantries','Food/Meals','Warming Center']

SERVICES_ON_SCHEDULE_KEY_STRING_DICT = {'Food/Pantries':'food_pantries_','Food/Meals':'food_meals_','Warming Center':'warming_center_'}

def create_day_bool(day, category_string):
    return st.checkbox(day, key=category_string + day)

def create_editable_df_for_schedule_entry(has_meals, service_key):
    is_available = []
    days = []
    meals = []
    open_times = []
    close_times = []
    if has_meals:
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
    else:
        is_available = [False for x in DAYS_OF_WEEK]
        open_times = ["" for x in DAYS_OF_WEEK]
        close_times = ["" for x in DAYS_OF_WEEK]
        df = pd.DataFrame(list(zip(DAYS_OF_WEEK, is_available, open_times, close_times)),
        columns =['day', 'available', 'beginning at', 'ending at'])
        return st.experimental_data_editor(df, key=service_key + '_weekly_schedule')
        
with open('available_services.txt') as f:
    for line in f.readlines():
        SERVICES_OPTIONS.append(line.strip())

with tab1:
    st.header('Enter Organization Information')
    st.subheader('Required Fields')
    name = st.text_input('Name')
    st.write('Location')
    address_line_one = st.text_input('Address')
    city = st.text_input('City')
    #state = st.text_input('State')
    zip_code = st.text_input('Zip Code')
    phone_num = st.text_input('Phone Number')

    #We Now have all the required fields. Create an organization object
    organization = Organization(name, address_line_one, city, zip_code, phone_num)

    st.subheader('Optional Fields')

    contact_name = st.text_input('Name of Contact')
    if contact_name:
        organization.set_contact(contact_name)
    email = st.text_input('Email')
    if email:
        organization.set_email(email)

    #Move onto services data entry
    st.header('Select Services Provided')
    for service in SERVICES_OPTIONS:
        service_checked = st.checkbox(service)

        #Outer if catches any items with a schedule
        #TODO: Re-approach so that editable dataframe is leveraged for user entry of schedules
        if service_checked and service in SERVICES_ON_SCHEDULE:
            service_key_string = SERVICES_ON_SCHEDULE_KEY_STRING_DICT[service]
            
            #create a weekly schedule object
            weekly_schedule = WeeklySchedule()
            #Editable df testing
            editable_df = None
            st.subheader(f"Enter Your {service} Schedule")
            st.write(":red[PLEASE NOTE: You must mark the 'available' column for any time slots you offer the service for it to be submitted.]")
            if service_key_string != 'food_meals_':
                editable_df = create_editable_df_for_schedule_entry(False, service_key_string)
                # st.write('Schedule Availability Preview')
                # st.dataframe(editable_df[editable_df['available']==True])
                for index, row in editable_df[editable_df['available']==True].iterrows():
                    daily_meal_schedule = DailySchedule(row['day'], row['beginning at'], row['ending at'])
                    weekly_schedule.add_daily_schedule(daily_meal_schedule)
                #Create the service, attach schedule to it, then attach service to organization
                service_obj = Service(service)
                service_obj.set_weekly_schedule(weekly_schedule)
                organization.add_service(service_obj)
            else:
                editable_df = create_editable_df_for_schedule_entry(True, service_key_string)
                # st.write('Schedule Availability Preview')
                # st.dataframe(editable_df[editable_df['available']==True])
                for index, row in editable_df[editable_df['available']==True].iterrows():
                    daily_meal_schedule = DailyMealSchedule(row['day'], row['beginning at'], row['ending at'], row['meal'])
                    weekly_schedule.add_daily_schedule(daily_meal_schedule)
                #Create the service, attach schedule to it, then attach service to organization
                service_obj = Service(service)
                service_obj.set_weekly_schedule(weekly_schedule)
                organization.add_service(service_obj)
        #If it's not one of the above services, we disregard schedules and just add the service
        elif service_checked:
            service_obj = Service(service)
            organization.add_service(service_obj)

    #Output current state of the record being entered to screen
    st.header("Record Preview:")
    st.write('This is what will be stored in the database upon submission based upon the information entered above.')
    st.subheader('General Information')
    st.write("---")
    #Create a series of dataframes based on the org dict
    for key, value in organization.__dict__.items():
        if key != 'services':
            st.write(f'{key} : {value}')
    st.write("---")
    st.subheader('Services Provided Information')
    st.write("---")
    for service in organization.__dict__['services']:
        st.write(service['name'])
        if service['has_schedule']:
            daily_schedules = service['weekly_schedule']['daily_schedules']
            #Output as a dataframe to the screen
            df = pd.json_normalize(daily_schedules)
            st.dataframe(df)
    st.write("---")
    #Use this as the developer view
    st.write('Developer View')
    st.json(organization.__dict__, expanded=False)