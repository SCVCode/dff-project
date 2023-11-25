import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Import the necessary Google Sheets API code_
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
def fetch_google_sheets_data():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=1)
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
st.title("Patient Data Dashboard")

# Dropdown for selecting patient
selected_patient_id = st.selectbox("Select Patient ID", data['Patient ID'].unique())

# Display patient information
patient_data = data[data['Patient ID'] == selected_patient_id]
st.write(f"**Patient ID:** {selected_patient_id}")
st.write(f"**Symptoms:** {patient_data['Symptoms'].values[0]}")
st.write(f"**Systolic BP:** {patient_data['Systolic BP'].values[0]}")
st.write(f"**Diastolic BP:** {patient_data['Diastolic BP'].values[0]}")
st.write(f"**Heart Rate:** {patient_data['Heart Rate'].values[0]}")
st.write(f"**Urine Analysis:** {patient_data['Urine Analysis'].values[0]}")

# Display data table
st.write("### Patient Data Table")
st.write(data[data['Patient ID'] == selected_patient_id])

# Create a line chart with multiple Y-axes
st.write("### Patient Vital Signs Over Time")
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=patient_data['Timestamp'], y=patient_data['Systolic BP'],
                         mode='lines', name='Systolic BP'), secondary_y=False)
fig.add_trace(go.Scatter(x=patient_data['Timestamp'], y=patient_data['Diastolic BP'],
                         mode='lines', name='Diastolic BP'), secondary_y=False)
fig.add_trace(go.Scatter(x=patient_data['Timestamp'], y=patient_data['Heart Rate'],
                         mode='lines', name='Heart Rate'), secondary_y=True)

# Update the layout for better visualization
fig.update_layout(title=f'Patient {selected_patient_id} Vital Signs Over Time',
                  xaxis_title='Timestamp',
                  yaxis_title='Blood Pressure (mmHg)',
                  yaxis2_title='Heart Rate (bpm)',
                  legend=dict(x=0, y=1))

# Reverse the Y-axis direction for both Y-axes
fig.update_yaxes(autorange="reversed", title_text="Blood Pressure (mmHg)", secondary_y=False)
fig.update_yaxes(autorange="reversed", title_text="Heart Rate (bpm)", secondary_y=True)

# Display the chart
st.plotly_chart(fig)

# Create the pie chart
st.write("### Urine Analysis Results")
result_counts = patient_data['Urine Analysis'].value_counts()
fig = px.pie(names=result_counts.index, values=result_counts.values, title='Urine Analysis Results')
st.plotly_chart(fig)
