import streamlit as st

try:
    from google.generativeai import GenerativeModel, configure as gemini_configure
except ImportError:
    GenerativeModel = None
    gemini_configure = None

with st.sidebar:
    gemini_api_key="AIzaSyBJUdcLlhcRnEW8qt3s6ha8kbSDT4YZH3o"

st.title("🔎 Gemini - Chat")

"""
This example uses Gemini to answer your questions. Web search is not available in this demo.
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a Gemini chatbot. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Ask me anything!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not gemini_api_key:
        st.info("Please add your Gemini API key to continue.")
        st.stop()

    if GenerativeModel is None or gemini_configure is None:
        st.error("google-generativeai package not installed. Install with 'pip install google-generativeai'.")
        st.stop()

    gemini_configure(api_key=gemini_api_key)
    history = "\n".join([
        ("User: " if m["role"] == "user" else "Assistant: ") + m["content"]
        for m in st.session_state["messages"]
    ])
    model = GenerativeModel("gemini-2.0-flash-001")
    try:
        response = model.generate_content(history + f"\nUser: {prompt}\nAssistant:")
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)
    except Exception as e:
        st.error(f"Gemini model error: {e}")
