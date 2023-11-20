import streamlit as st
import pandas as pd
import toml
from streamlit_gsheets import GSheetsConnection
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up Google Sheets API credentials and parameters
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SAMPLE_SPREADSHEET_ID = '1ldETnrsYXn0RdrrhwdH-xW3PO_SdHQBz_v6qMf_CT9U'
SAMPLE_RANGE_NAME = 'form_responses!A2:U'

# Load credentials from secrets.toml
with open('secrets.toml', 'r') as f:
    secrets = toml.load(f)

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch data from Google Sheets
def fetch_google_sheets_data():
    creds = Credentials.from_authorized_user_info(secrets['google_sheets'], SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
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
