import streamlit as st
import json
import pandas as pd
from organization import Organization
from service import Service
from weekly_schedule import WeeklySchedule
from daily_schedule import DailySchedule, DailyMealSchedule



tab3, tab2, tab1 = st.tabs(["Version 3", "Vesion 2", "Version 1"])

SERVICES_OPTIONS = []

DAYS_OF_WEEK = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

MEALS = ["Breakfast", "Lunch", "Dinner"]

with open('available_services.txt') as f:
    for line in f.readlines():
        SERVICES_OPTIONS.append(line.strip())

with tab3:
    st.subheader('Enter Organization Information')
    st.write("---")
    st.markdown('Required Fields')
    name = st.text_input('Name')
    st.write('Location')
    address_line_one = st.text_input('Address Line 1')
    #address_line_two = st.text_input('Address Line 2')
    city = st.text_input('City')
    #state = st.text_input('State')
    zip_code = st.text_input('Zip Code')
    phone_num = st.text_input('Phone Number')

    #We Now have all the required fields. Create an organization object
    organization = Organization(name, address_line_one, city, zip_code, phone_num)

    st.markdown('Optional Fields')

    contact_name = st.text_input('Name of Contact')
    if contact_name:
        organization.set_contact(contact_name)
    email = st.text_input('Email')
    if email:
        organization.set_email(email)

    #Move onto services data entry
    st.subheader('Select Services Provided')
    st.write("---")
    for service in SERVICES_OPTIONS:
        service_checked = st.checkbox(service)
        if service_checked and service == "Food/Meals":
            #create a weekly schedule object
            weekly_schedule = WeeklySchedule()
            st.write('Food / Meals Schedule:')
            for day in DAYS_OF_WEEK:
                day_flag = st.checkbox(day, key='food_meals_'+day)
                if day_flag:
                    #create a daily meal schedule
                    for meal in MEALS:
                        meal_flag = st.checkbox(meal, key='food_meals_'+ day + '_' + meal)
                        if meal_flag:
                            start_time = st.text_input(f'Beginning at what time?', key='food_meals_'+ day + '_start_time')
                            stop_time = st.text_input(f'Ending at what time?', key='food_meals_'+ day + '_stop_time')
                            daily_meal_schedule = DailyMealSchedule(day, start_time, stop_time, meal)
                            st.write(daily_meal_schedule.__dict__)
                            #add the daily meal schedule to the weekly schedule
                            weekly_schedule.add_daily_schedule(daily_meal_schedule)
                            st.write(weekly_schedule.__dict__)
            #create a service object, attach weekly schedule to it then add the service object to the org
            service = Service(service)
            service.set_weekly_schedule(weekly_schedule)
            organization.add_service(service)
            st.write("---")
        #repeat for other items where we are capturing schedules
        elif service_checked and service == "Food/Pantries":
            #create a weekly schedule object
            weekly_schedule = WeeklySchedule()
            st.write('Food / Pantries Schedule:')
            for day in DAYS_OF_WEEK:
                day_flag = st.checkbox(day, key='food_pantries_'+day)
                if day_flag:
                    #create a daily schedule
                    start_time = st.text_input(f'Beginning at what time?', key='food_pantries_'+ day + '_start_time')
                    stop_time = st.text_input(f'Ending at what time?', key='food_pantries_'+ day + '_stop_time')
                    daily_schedule = DailySchedule(day, start_time, stop_time)
                    weekly_schedule.add_daily_schedule(daily_schedule)
            service = Service(service)
            service.set_weekly_schedule(weekly_schedule)
            organization.add_service(service)
            st.write("---")
        elif service_checked and service == "Warming Center":
            #create a weekly schedule object
            weekly_schedule = WeeklySchedule()
            st.write('Warming Center Schedule:')
            for day in DAYS_OF_WEEK:
                day_flag = st.checkbox(day, key='warming_center_'+day)
                if day_flag:
                    #Create a daily schedule
                    start_time = st.text_input(f'Beginning at what time?', key='warming_center_'+ day + '_start_time')
                    stop_time = st.text_input(f'Ending at what time?', key='warming_center_'+ day + '_stop_time')
                    daily_schedule = DailySchedule(day, start_time, stop_time)
                    weekly_schedule.add_daily_schedule(daily_schedule)
            service = Service(service)
            service.set_weekly_schedule(weekly_schedule)
            organization.add_service(service)
            st.write("---")
        elif service_checked:
            #If it's not one of the above services, we disregard schedules and just add the service
            service = Service(service)
            organization.add_service(service)

    st.subheader("Record Preview:")
    st.write(organization.__dict__)

# with tab2:
#     st.markdown('Enter Organization Information')

#     name = st.text_input('Name')
#     st.write('Location')
#     address_line_one = st.text_input('Address Line 1')
#     address_line_two = st.text_input('Address Line 2')
#     city = st.text_input('City')
#     state = st.text_input('State')
#     zip_code = st.text_input('Zip Code')

#     phone_num = st.text_input('Phone Number')
#     contact_name = st.text_input('Name of Contact')

#     email = st.text_input('Email')

#     st.write('Services Provided')

#     for service in SERVICES_OPTIONS:
#         service_checked = st.checkbox(service)
#         if service_checked and service == "Food/Meals":
#             st.write('Food / Meals Schedule:')
#             for day in DAYS_OF_WEEK:
#                 day_flag = st.checkbox(day, key='food_meals_'+day)
#                 if day_flag:
#                     time_open = st.text_input(f'Open Times on {day}', key='food_meals_'+ day + '_time')
#             st.write("---")
#         #repeat for other items where we are capturing schedules
#         if service_checked and service == "Food/Pantries":
#             st.write('Food / Pantries Schedule:')
#             for day in DAYS_OF_WEEK:
#                 day_flag = st.checkbox(day, key='food_pantries_'+day)
#                 if day_flag:
#                     time_open = st.text_input(f'Open Times on {day}', key='food_pantries_'+ day + '_time')
#             st.write("---")
#         if service_checked and service == "Warming Center":
#             st.write('Warming Center Schedule:')
#             for day in DAYS_OF_WEEK:
#                 day_flag = st.checkbox(day, key='warming_center_'+day)
#                 if day_flag:
#                     time_open = st.text_input(f'Open Times on {day}', key='warming_center_'+ day + '_time')
#             st.write("---")

# #Tab with initial version shown
# with tab1:
#     st.markdown("Enter Housing Agency Info")

#     #init session state
#     if 'waiting_periods_num' not in st.session_state:
#         st.session_state.waiting_periods_num = 1

#     MONTH_LIST = ['January','February','March','April','May','June','July','August',
#                 'September','October','November','December']

#     #with st.form("add_housing_agency"):
#     name = st.text_input('Agency Name')
#     _type = st.selectbox('Agency Type', ['Section 8', 'Private'])
#     location = st.text_input('Location') #May need to allow for entry of an array of locations
#     contact_number = st.text_input('Contact Number')
#     has_application_period = st.checkbox("Has Application Period")
#     if has_application_period:
#         application_start_date = st.date_input('Start Date')
#         application_end_date = st.date_input('End Date')
#     has_waiting_period = st.checkbox("Has Waiting Period")
#     if has_waiting_period:
#         st.write('Select Waiting Period Quantity')
#         number_of_waiting_periods = st.number_input('# of Waiting Periods',min_value=1, key='waiting_periods_num')
#         #TODO: instantiate an empty data structure to write user entry into
#         waiting_periods_array = []
#         for num in range(st.session_state.waiting_periods_num):
#             st.write('Number of Bedrooms')
#             number_bedrooms = st.number_input(f'# of Bedrooms for instance #{num + 1}', min_value=1)
#             range_in_months = st.slider(f'Select estimated wait in months for instance #{num + 1}', 1, 12, (1,3))
#             waiting_periods_array.append({'number_of_beds':number_bedrooms, 'range_in_months':range_in_months})
#     qualifications = st.text_area('Qualifications') #Refactor into a multi select box

#         #submitted = st.form_submit_button("Submit")
#     submit = st.button('Submit Housing Agency Info')
#     if submit:
#         st.write('Submitted Record:')
#             #with open('housing_agencoes.json', 'r+') as jf:
#         housing_agency_dict = {'name':name,'type':_type, 'location':location , 'contact_number':contact_number, 
#                     'has_application_period':has_application_period, 'application_start_date':application_start_date,
#                     'application_end_date':application_end_date, 'has_waiting_period':has_waiting_period,
#                     'waiting_periods_array':waiting_periods_array, 'qualifications':qualifications}
#         st.write(housing_agency_dict)
#         #file_data = json.load(jf)
#         #file_data.append(pr_dict)
#         #jf.seek(0)
#         #json.dump(file_data, jf, indent=2)
#         #st.balloons()
