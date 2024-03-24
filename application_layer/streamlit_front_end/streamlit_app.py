import streamlit as st
import pandas as pd
import os
import requests

BASE_URL = os.getenv('BASE_URL')

st.set_page_config(page_title='Loan Eligibility Prediction', page_icon='🏠', layout='wide', initial_sidebar_state='auto')

st.title('Loan Eligibility Prediction 🏠')

with st.form(key='loan_form'):
    st.header('Please enter your details:')
    
    applicant_income = st.number_input('Applicant Income', min_value=0.0, step=100.0, format="%.2f")
    coapplicant_income = st.number_input('Coapplicant Income', min_value=0.0, value=0.0, step=100.0, format="%.2f")
    loan_amount = st.number_input('Loan Amount', min_value=0.0, step=1000.0, format="%.3f")
    loan_amount_term = st.number_input('Loan Amount Term', min_value=0.0, step=1.0, format="%.1f")

    credit_history = st.radio('Credit History', options=['Yes', 'No'])
    dependents = st.selectbox('Dependents', options=['0','1','2','3+'])
    education = st.radio('Education', options=['Graduate', 'Not Graduate'])
    married = st.radio('Married', options=['Yes', 'No'])
    property_area = st.selectbox('Property Area', options=['Rural', 'Semiurban', 'Urban'])

    get_prediction = st.form_submit_button(label='Check Eligibility')
    get_previous_predictions = st.form_submit_button(label='Get Past Predictions')

    if get_prediction:
        form_data = {
            'ApplicantIncome': applicant_income,
            'CoapplicantIncome': coapplicant_income,
            'LoanAmount': loan_amount,
            'Loan_Amount_Term': loan_amount_term,
            'Credit_History': 1 if credit_history == 'Yes' else 0,
            'Dependents': dependents,
            'Education': education,
            'Married': married,
            'Property_Area': property_area
        }
        response = requests.post(BASE_URL + '/predict', json=form_data)
        if response.status_code == 200:
            prediction = response.json()
            st.success(f'Eligibility prediction: {prediction}')
        else:
            st.error('Failed to get prediction from the API.')

    if get_previous_predictions:
        response = requests.get(BASE_URL + '/get-past-predictions')
        if response.status_code == 200:
            predictions_data = pd.DataFrame(response.json())
            st.table(predictions_data)
        else:
            st.error('Failed to retrieve past predictions.')
