import streamlit as st

st.title("Welcome Back!")

col1, col2, col3 = st.columns(3)

col1.link_button("Go to Active Users", "https://streamlit.io/active_users", value =120)
col2.link_button("Go to Non-Compliant Users", "https://streamlit.io/non_compliant_users", value =120)
col3.link_button("Go to Clinical Alerts", "https://streamlit.io/clinicalalerts", value = 120)

