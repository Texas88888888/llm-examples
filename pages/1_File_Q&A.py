import streamlit as st

try:
    from google.generativeai import GenerativeModel, configure as gemini_configure
except ImportError:
    GenerativeModel = None
    gemini_configure = None

with st.sidebar:
    gemini_api_key ="AIzaSyBJUdcLlhcRnEW8qt3s6ha8kbSDT4YZH3o"

st.title("📝 File Q&A with Gemini")
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))
question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question and not gemini_api_key:
    st.info("Please add your Gemini API key to continue.")

if uploaded_file and question and gemini_api_key:
    if GenerativeModel is None or gemini_configure is None:
        st.error("google-generativeai package not installed. Install with 'pip install google-generativeai'.")
        st.stop()
    gemini_configure(api_key=gemini_api_key)
    article = uploaded_file.read().decode()
    prompt = f"Here's an article:\n\n{article}\n\n{question}"
    model = GenerativeModel("gemini-2.0-flash-001")
    try:
        response = model.generate_content(prompt)
        st.write("### Answer")
        st.write(response.text)
    except Exception as e:
        st.error(f"Error generating response: {e}")
