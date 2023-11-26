import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

from streamlit.hello.utils import show_code


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
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
            return []
        return values
    except HttpError as err:
        print(err)
        return []

# Load data from Google Sheets
data = pd.DataFrame(fetch_google_sheets_data(), columns=[
    'Timestamp', 'Patient ID',
    'Symptoms',
    'Systolic BP',
    'Diastolic BP',
    'Heart Rate',
    'Urine Analysis'
])

# Streamlit app layout
st.title("Patient Continuous DataStream")

st.dataframe(data, use_container_width=True)



fetch_google_sheets_data()

