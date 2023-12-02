import streamlit as st
import toml
from login import authenticator

# Load theme configuration from config.toml
with open('config.toml', 'r') as config_file:
    theme_config = toml.load(config_file).get('theme', {})

# Access theme options from the configuration or use default values
primary_color = theme_config.get('primaryColor', '#F63366')
background_color = theme_config.get('backgroundColor', '#FFFFFF')

# Apply theme configuration to Streamlit using st.markdown for CSS styles
st.markdown(
    f"""
    <style>
        body {{
            color: black;
        }}
        .css-1vqrsj9, .st-cv, .st-ai, .st-jg, .st-hg, .st-co, .st-cp, .st-go, .st-ea, .st-ew {{
            color: {primary_color} !important;
        }}
        .stApp {{
            background-color: {background_color} !important;
        }}
        .st-cg, .st-bi, .st-gp, .st-gh, .st-cm, .st-kp, .st-iw, .st-hw, .st-gp, .st-dx, .st-kq, .st-jj, .st-gf, .st-it, .st-ij {{
            background-color: {primary_color} !important;
            color: #FFFFFF !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# The rest of your Streamlit app code
def run():
    st.write("# Welcome to your Patient Dashboard! 👋")

    st.sidebar.success("Select a View above.")
    
    st.sidebar.link_button("Add new Patient", 'https://docs.google.com/forms/d/15u76uURRcv1q0en3A9e1-CFumbb3iLzQr0IMXZXh_1w/edit')

    st.markdown("""
        This is a demo of the patient monitoring dashboard that would be used to remotely monitor patients with or at risk of hypertensive disorders of pregnancy in Zimbabwe
    """)

    # Add the login functionality here
    authenticator.login('Login', 'main')


if __name__ == "__main__":
    run()

