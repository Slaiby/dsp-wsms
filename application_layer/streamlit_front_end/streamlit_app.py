import json
import streamlit as st
import pandas as pd
import os
import requests
from tempfile import NamedTemporaryFile

BASE_URL = os.getenv('BASE_URL')

st.set_page_config(
    page_title='Loan Eligibility Prediction',
    page_icon='🏠',
    layout='wide', 
    initial_sidebar_state='auto' 
)

def prediction_page():
    st.write("House Loan Prediction Page")

    with st.form(key='prediction_form'):
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

    # Upload CSV file for multiple predictions
    uploaded_file = st.file_uploader("Upload CSV file for multiple predictions", type=['csv'])

    # file size check
    if uploaded_file is not None and uploaded_file.size > 200 * 1024 * 1024:  # 200MB in bytes
        st.error("File size exceeds the maximum limit of 200MB. Please upload a smaller file.")
        return

    # Predict button for CSV file
    if uploaded_file is not None:
        predict_button = st.button("Predict for CSV File")
    else:
        predict_button = st.button("Predict for CSV File", disabled=True)

    # Process the uploaded CSV file if it exists
    if predict_button and uploaded_file is not None:
        temp_file = None

    try:
        # Saving the uploaded file temporarily with its original name
        temp_file = NamedTemporaryFile(delete=False, suffix='.csv')

        # Checking if uploaded_file has content before reading from it
        if uploaded_file:
            uploaded_file_content = uploaded_file.read()

            if uploaded_file_content:
                temp_file.write(uploaded_file_content)
                
                # Sending the file to the upload endpoint
                upload_response = requests.post(BASE_URL + '/file/upload', files={'file': (uploaded_file.name, open(temp_file.name, 'rb'))})
                if upload_response.status_code == 200:
                    st.success("File uploaded successfully.")

                    # Proceed with predictions using the uploaded file
                    csv_data = pd.read_csv(temp_file.name, encoding='latin1')
                    st.write("Predictions for uploaded CSV file:")
                    st.write(csv_data)
                else:
                    st.error("Failed to upload file. Please try again.")
            else:
                st.error("Uploaded file is empty.")


    finally:
        # Cleaning up the temporary file
        if temp_file:
            temp_file.close()
            os.unlink(temp_file.name)

        elif predict_button:
            st.error("Please upload a CSV file before predicting.")


    # Make prediction for single entry if prediction form is submitted
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

def past_predictions_page():
    # Date selection components
    start_date = st.date_input("Start Date", value=None)
    end_date = st.date_input("End Date", value=None)

    # Prediction source drop list
    prediction_source = st.selectbox("Prediction Source", options=["webapp", "scheduled predictions", "all"])

    # Get past predictions button
    with st.form(key='past_predictions_form'):
        get_previous_predictions = st.form_submit_button(label='Get Past Predictions')

        if get_previous_predictions:
            # Prepare query parameters based on user input
            query_params = {
                "start_date": start_date.strftime('%Y-%m-%d') if start_date else None,
                "end_date": end_date.strftime('%Y-%m-%d') if end_date else None,
                "prediction_source": prediction_source
            }

            # API request to retrieve past predictions
            response = requests.get(BASE_URL + '/get-past-predictions', params=query_params)
            if response.status_code == 200:
                predictions_data = pd.DataFrame(response.json())

                summary_df = predictions_data[['id', 'prediction', 'timestamp']]
                st.table(summary_df)

                st.write("Detailed JSON Data:")
                for index, row in predictions_data.iterrows():
                    with st.expander(f"Details for Prediction ID {row['id']}"):
                        st.json(row['result'])
            else:
                st.error('Failed to retrieve past predictions.')

def main():
    st.title("Loan Eligibility Prediction 🏠")

    page = st.sidebar.selectbox("Select Page", ["Prediction", "Past Predictions"])

    # Display selected page
    if page == "Prediction":
        prediction_page()
    elif page == "Past Predictions":
        past_predictions_page()


if __name__ == "__main__":
    main()