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

SERVICES_ON_SCHEDULE = ['Food/Pantries','Food/Meals','Warming Center']

SERVICES_ON_SCHEDULE_KEY_STRING_DICT = {'Food/Pantries':'food_pantries_','Food/Meals':'food_meals_','Warming Center':'warming_center_'}

def create_day_bool(day, category_string):
    return st.checkbox(day, key=category_string + day)

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
        #TODO: Refactor this if / elif and nested logic.
        #Proobably could refactor into a single if with an inner if
        #Outer if catches any items with a schedule
        if service_checked and service in SERVICES_ON_SCHEDULE:
            service_key_string = SERVICES_ON_SCHEDULE_KEY_STRING_DICT[service]

            #create a weekly schedule object
            weekly_schedule = WeeklySchedule()
            st.write(f'{service} Schedule: ' )
            for day in DAYS_OF_WEEK:
                day_flag = create_day_bool(day, service_key_string)
                if day_flag:
                    #Create a daily schedule
                    #Inner if to handle if it is a meal schedule
                    if service_key_string == 'food_meals_':
                        for meal in MEALS:
                            meal_flag = st.checkbox(meal, key='food_meals_'+ day + '_' + meal)
                            if meal_flag:
                                start_time = st.text_input(f'Beginning at what time?', key=service_key_string + day + '_'+ meal + '_start_time')
                                stop_time = st.text_input(f'Ending at what time?', key=service_key_string + day + '_'+ meal + '_stop_time')
                                daily_meal_schedule = DailyMealSchedule(day, start_time, stop_time, meal)
                                st.write(daily_meal_schedule.__dict__)
                                #add the daily meal schedule to the weekly schedule
                                weekly_schedule.add_daily_schedule(daily_meal_schedule)
                                st.write(weekly_schedule.__dict__)
                    #Handle non meal related daily schedules
                    else:
                        start_time = st.text_input(f'Beginning at what time?', key=service_key_string + day + '_start_time')
                        stop_time = st.text_input(f'Ending at what time?', key=service_key_string + day + '_stop_time')
                        daily_schedule = DailySchedule(day, start_time, stop_time)
                        weekly_schedule.add_daily_schedule(daily_schedule)
            #Create the service, attach schedule to it, then attach service to organization
            service = Service(service)
            service.set_weekly_schedule(weekly_schedule)
            organization.add_service(service)
        #If it's not one of the above services, we disregard schedules and just add the service
        elif service_checked:
            service = Service(service)
            organization.add_service(service)
    #Output current state of the record being entered to screen
    st.subheader("Record Preview:")
    st.write(organization.__dict__)