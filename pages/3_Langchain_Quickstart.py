import streamlit as st

try:
    from google.generativeai import GenerativeModel, configure as gemini_configure
except ImportError:
    GenerativeModel = None
    gemini_configure = None

st.title("🦜🔗 Gemini Quickstart App")

with st.sidebar:
    gemini_api_key = "AIzaSyBJUdcLlhcRnEW8qt3s6ha8kbSDT4YZH3o"


def generate_response(input_text):
    if GenerativeModel is None or gemini_configure is None:
        st.error("google-generativeai package not installed. Install with 'pip install google-generativeai'.")
        return
    gemini_configure(api_key=gemini_api_key)
    model = GenerativeModel("gemini-2.0-flash-001")
    try:
        response = model.generate_content(input_text)
        st.info(response.text)
    except Exception as e:
        st.error(f"Gemini error: {e}")


with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    if not gemini_api_key:
        st.info("Please add your Gemini API key to continue.")
    elif submitted:
        generate_response(text)
