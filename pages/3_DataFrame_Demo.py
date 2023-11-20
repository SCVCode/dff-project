import os
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from streamlit_gsheets import GSheetsConnection
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up Google Sheets API credentials and parameters
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SAMPLE_SPREADSHEET_ID = '1ldETnrsYXn0RdrrhwdH-xW3PO_SdHQBz_v6qMf_CT9U'
SAMPLE_RANGE_NAME = 'form_responses!A2:U'

# Load credentials from credentials.json
credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch data from Google Sheets
def fetch_google_sheets_data():
    try:
        service = build('sheets', 'v4', credentials=credentials)
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

# Read data from Google Sheets
df = pd.DataFrame(fetch_google_sheets_data())

# Display the DataFrame
st.dataframe(df)

st.set_page_config(page_title="Patient Record Page Demo", page_icon="📊")
st.markdown("Patient Records")
st.sidebar.header("Patient Records")
st.write(
    """This page shows the list of all Patient Records but can be filtered according to the patient name or warning messages (high measurements reported) """
)
