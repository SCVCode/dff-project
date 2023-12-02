import streamlit as st
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

# Set up Google Sheets API credentials and parameters
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SAMPLE_SPREADSHEET_ID = '1zdI8XWKCkjGGdfe2L7O5dB-j-G6wTfpX571xiJxD_GM'
SAMPLE_RANGE_NAME = 'form_responses!A2:G'

# Fetch data from Google Sheets
@st.cache_data
def fetch_google_sheets_data():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=10000)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        if not values:
            st.warning('No data found in the Google Sheet.')
            return pd.DataFrame()  # Return an empty DataFrame if no data is found
        return pd.DataFrame(values[1:], columns=values[0])
    except HttpError as err:
        st.error(f'Error fetching data from Google Sheets: {err}')
        return pd.DataFrame()

# Load data from Google Sheets
data = pd.DataFrame(fetch_google_sheets_data(), columns=[
    'Timestamp', 
    'Patient ID',
    'Symptoms',
    'Systolic BP',
    'Diastolic BP',
    'Heart Rate',
    'Urine Analysis'
])

# Streamlit app layout
st.title("Patient Continuous DataStream")

# Display the original data
st.header("Original Data:")
st.dataframe(data, use_container_width=True)

# Buttons for navigation
col1, col2, col3 = st.columns(3)

# Function to filter data based on conditions
def filter_data(condition):
    if condition == 'Active Users':
        return data[data['Patient ID'].isin(data['Patient ID'].value_counts()[data['Patient ID'].value_counts() >= 3].index)]
    elif condition == 'Non-Compliant Users':
        return data[data['Patient ID'].isin(data['Patient ID'].value_counts()[data['Patient ID'].value_counts() <= 2].index)]
    elif condition == 'Clinical Alerts':
        return data[data['Systolic BP'].astype(float) > 150]
    else:
        return data

# Button to filter for Active Users
if col1.button("Go to Active Users"):
    filtered_data = filter_data('Active Users')
    st.header("Active Users (Patient ID appears 3 or more times):")
    st.dataframe(filtered_data, use_container_width=True)

# Button to filter for Non-Compliant Users
if col2.button("Go to Non-Compliant Users"):
    filtered_data = filter_data('Non-Compliant Users')
    st.header("Non-Compliant Users (Patient ID appears 2 or fewer times):")
    st.dataframe(filtered_data, use_container_width=True)

# Button to filter for Clinical Alerts
if col3.button("Go to Clinical Alerts"):
    filtered_data = filter_data('Clinical Alerts')
    st.header("Clinical Alerts (Systolic BP > 150):")
    st.dataframe(filtered_data, use_container_width=True)
