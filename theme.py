import streamlit as st
import toml

def apply_custom_theme():
    # Load theme configuration from config.toml
    with open('config.toml', 'r') as config_file:
        theme_config = toml.load(config_file).get('theme', {})

    # Access theme options from the configuration or use default values
    primary_color = theme_config.get('primaryColor', '#F63366')
    background_color = theme_config.get('backgroundColor', '#FFFFFF')
    border_color = theme_config.get('borderColor', '#FF69B4')
    table_border_color = theme_config.get('tableBorderColor', '#FF69B4')
    button_border_color = theme_config.get('buttonBorderColor', '#FF69B4')
    widget_border_color = theme_config.get('widgetBorderColor', '#FF69B4')

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
                border-color: {border_color} !important;
            }}
            .stTable {{
                border-color: {table_border_color} !important;
            }}
            .stButton {{
                border-color: {button_border_color} !important;
            }}
            .stWidget {{
                border-color: {widget_border_color} !important;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )