import streamlit as st
import pandas as pd
import os
import requests  # Import requests

data = pd.read_csv(os.getcwd() + '/logic_layer/data/loan_data.csv')

st.set_page_config(page_title='Loan Eligibility Prediction', page_icon='🏠', layout='wide', initial_sidebar_state='auto')

st.title('Loan Eligibility Prediction 🏠')

with st.form(key='loan_form'):
    st.header('Please enter your details:')
    
    credit_history = st.number_input('Credit History', min_value=0.0, format="%.1f")
    dependents = st.selectbox('Dependents', options=data['Dependents'].unique(), index=int(data['Dependents'].mode()[0]))
    education = st.radio('Education', options=data['Education'].unique(), index=int((data['Education'] == data['Education'].mode()[0]).argmax()))
    married = st.radio('Married', options=data['Married'].unique(), index=int((data['Married'] == data['Married'].mode()[0]).argmax()))
    property_area = st.number_input('Property Area', min_value=0)
    coapplicant_income = st.number_input('Coapplicant Income', min_value=0.0, value=0.0, step=100.0, format="%.2f")
    get_prediction = st.form_submit_button(label='Check Eligibility')
    get_previous_predictions = st.form_submit_button(label='Get Past Predictions')

if get_prediction:
    form_data = {
        'credit_history': credit_history,
        'dependents': dependents,
        'education': education,
        'married': married,
        'property_area': property_area,
        'coapplicant_income': coapplicant_income
    }
    
    response = requests.post('http://127.0.0.1:8000/predict', json=form_data)
    
    if response.status_code == 200:
        prediction = response.json()
        st.success(f'Eligibility prediction: {prediction}')
    else:
        st.error('Failed to get prediction from the API.')

if get_previous_predictions:
    response = requests.get('http://127.0.0.1:8000/get-past-predictions')
    
    if response.status_code == 200:
        predictions_data = pd.DataFrame(response.json())
        
        st.table(predictions_data)
    else:
        st.error('Failed to retrieve past predictions.')
