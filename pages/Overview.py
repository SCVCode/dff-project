import streamlit as st

st.title("Welcome Back!")

col1, col2, col3 = st.columns(3)

tab1 = st.link_button("Go to Active Users", "https://streamlit.io/active_users")
tab2 = st.link_button("Go to Non-Compliant Users", "https://streamlit.io/non_compliant_users")
tab3 = st.link_button("Go to Clinical Alerts", "https://streamlit.io/clinicalalerts")

col1.header = ("tab1")
col2.header = ("tab2")
col3.header = ("tab3")

