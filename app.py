import streamlit as st
import json

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