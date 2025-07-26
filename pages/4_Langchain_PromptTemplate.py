import streamlit as st

try:
    from google.generativeai import GenerativeModel, configure as gemini_configure
except ImportError:
    GenerativeModel = None
    gemini_configure = None

st.title("🦜🔗 Langchain - Blog Outline Generator App")

gemini_api_key = "AIzaSyBJUdcLlhcRnEW8qt3s6ha8kbSDT4YZH3o"


def blog_outline(topic):
    if GenerativeModel is None or gemini_configure is None:
        st.error("google-generativeai package not installed. Install with 'pip install google-generativeai'.")
        return
    gemini_configure(api_key=gemini_api_key)
    template = (
        "As an experienced data scientist and technical writer, generate an outline for a blog about {topic}."
    )
    prompt = template.format(topic=topic)
    model = GenerativeModel("gemini-2.0-flash-001")
    try:
        response = model.generate_content(prompt)
        return st.info(response.text)
    except Exception as e:
        st.error(f"Gemini error: {e}")


with st.form("myform"):
    topic_text = st.text_input("Enter prompt:", "")
    submitted = st.form_submit_button("Submit")
    if not gemini_api_key:
        st.info("Please add your Gemini API key to continue.")
    elif submitted:
        blog_outline(topic_text)
