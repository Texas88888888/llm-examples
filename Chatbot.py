import streamlit as st

try:
    from google.generativeai import GenerativeModel, configure as gemini_configure
except ImportError:
    GenerativeModel = None
    gemini_configure = None

with st.sidebar:
    gemini_api_key = "AIzaSyBJUdcLlhcRnEW8qt3s6ha8kbSDT4YZH3o"
    st.markdown("[Get a Gemini API key](https://aistudio.google.com/app/apikey)")
    st.markdown("[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)")
    st.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)")

st.title("🐄 Austin's Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Mooshy")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Can I help you today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input("Type your message here...", key="main_chat_input")
if prompt:
    if not gemini_api_key:
        st.info("Please add your Gemini API key to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if GenerativeModel is None or gemini_configure is None:
        st.error("google-generativeai package not installed. Install with 'pip install google-generativeai'.")
        st.stop()
    gemini_configure(api_key=gemini_api_key)
    history = "\n".join([
        ("User: " if m["role"] == "user" else "Assistant: ") + m["content"]
        for m in st.session_state.messages
    ])
    model = GenerativeModel("gemini-2.0-flash-001")
    try:
        gemini_response = model.generate_content(history + f"\nUser: {prompt}\nAssistant:")
        msg = gemini_response.text
    except Exception as e:
        st.error(f"Gemini error: {e}")
        st.stop()

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
