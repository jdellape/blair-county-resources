import streamlit as st
import json
import pandas as pd


tab2, tab1 = st.tabs(["Vesion 2", "Version 1"])

SERVICES_OPTIONS = []

DAYS_OF_WEEK = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

with open('available_services.txt') as f:
    for line in f.readlines():
        SERVICES_OPTIONS.append(line.strip())

with tab2:
    st.markdown('Enter Organization Information')

    name = st.text_input('Name')
    st.write('Location')
    address_line_one = st.text_input('Address Line 1')
    address_line_two = st.text_input('Address Line 2')
    city = st.text_input('City')
    state = st.text_input('State')
    zip_code = st.text_input('Zip Code')

    phone_num = st.text_input('Phone Number')
    contact_name = st.text_input('Name of Contact')

    email = st.text_input('Email')

    st.write('Services Provided')

    for service in SERVICES_OPTIONS:
        service_checked = st.checkbox(service)
        if service_checked and service == "Food/Meals":
            st.write('Food / Meals Schedule:')
            for day in DAYS_OF_WEEK:
                day_flag = st.checkbox(day, key='food_meals_'+day)
                if day_flag:
                    time_open = st.text_input(f'Open Times on {day}', key='food_meals_'+ day + '_time')
            st.write("---")
        #repeat for other items where we are capturing schedules
        if service_checked and service == "Food/Pantries":
            st.write('Food / Pantries Schedule:')
            for day in DAYS_OF_WEEK:
                day_flag = st.checkbox(day, key='food_pantries_'+day)
                if day_flag:
                    time_open = st.text_input(f'Open Times on {day}', key='food_pantries_'+ day + '_time')
            st.write("---")
        if service_checked and service == "Warming Center":
            st.write('Warming Center Schedule:')
            for day in DAYS_OF_WEEK:
                day_flag = st.checkbox(day, key='warming_center_'+day)
                if day_flag:
                    time_open = st.text_input(f'Open Times on {day}', key='warming_center_'+ day + '_time')
            st.write("---")

#Tab with initial version shown
with tab1:
    st.markdown("Enter Housing Agency Info")

    #init session state
    if 'waiting_periods_num' not in st.session_state:
        st.session_state.waiting_periods_num = 1

    MONTH_LIST = ['January','February','March','April','May','June','July','August',
                'September','October','November','December']

    #with st.form("add_housing_agency"):
    name = st.text_input('Agency Name')
    _type = st.selectbox('Agency Type', ['Section 8', 'Private'])
    location = st.text_input('Location') #May need to allow for entry of an array of locations
    contact_number = st.text_input('Contact Number')
    has_application_period = st.checkbox("Has Application Period")
    if has_application_period:
        application_start_date = st.date_input('Start Date')
        application_end_date = st.date_input('End Date')
    has_waiting_period = st.checkbox("Has Waiting Period")
    if has_waiting_period:
        st.write('Select Waiting Period Quantity')
        number_of_waiting_periods = st.number_input('# of Waiting Periods',min_value=1, key='waiting_periods_num')
        #TODO: instantiate an empty data structure to write user entry into
        waiting_periods_array = []
        for num in range(st.session_state.waiting_periods_num):
            st.write('Number of Bedrooms')
            number_bedrooms = st.number_input(f'# of Bedrooms for instance #{num + 1}', min_value=1)
            range_in_months = st.slider(f'Select estimated wait in months for instance #{num + 1}', 1, 12, (1,3))
            waiting_periods_array.append({'number_of_beds':number_bedrooms, 'range_in_months':range_in_months})
    qualifications = st.text_area('Qualifications') #Refactor into a multi select box

        #submitted = st.form_submit_button("Submit")
    submit = st.button('Submit Housing Agency Info')
    if submit:
        st.write('Submitted Record:')
            #with open('housing_agencoes.json', 'r+') as jf:
        housing_agency_dict = {'name':name,'type':_type, 'location':location , 'contact_number':contact_number, 
                    'has_application_period':has_application_period, 'application_start_date':application_start_date,
                    'application_end_date':application_end_date, 'has_waiting_period':has_waiting_period,
                    'waiting_periods_array':waiting_periods_array, 'qualifications':qualifications}
        st.write(housing_agency_dict)
        #file_data = json.load(jf)
        #file_data.append(pr_dict)
        #jf.seek(0)
        #json.dump(file_data, jf, indent=2)
        #st.balloons()
