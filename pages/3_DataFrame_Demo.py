
from urllib.error import URLError

import altair as alt
import pandas as pd

import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read()

# Print results.
for row in df.itertuples():
    st.write(f"{row.name} has a :{row.pet}:")


st.set_page_config(page_title="Patient Record Page Demo", page_icon="📊")
st.markdown(" Patient Records")
st.sidebar.header("Patient Records")
st.write(
    """This page shows the list of all Patient Records but can be filtered according to the patient name or warning messages (high measurements reported) """
)

# Call the Streamlit app function
if __name__ == '__main__':
    data_frame_demo()
