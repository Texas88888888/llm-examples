from openai import OpenAI
import streamlit as st
from streamlit_feedback import streamlit_feedback
import trubrics

try:
    from google.generativeai import GenerativeModel, configure as gemini_configure
except ImportError:
    GenerativeModel = None
    gemini_configure = None

with st.sidebar:
    gemini_api_key = "AIzaSyBJUdcLlhcRnEW8qt3s6ha8kbSDT4YZH3o"

st.title("📝 Chat with feedback (Trubrics)")

"""
In this example, we're using [streamlit-feedback](https://github.com/trubrics/streamlit-feedback) and Trubrics to collect and store feedback
from the user about the Gemini responses.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you? Leave feedback to help me improve!"}
    ]
if "response" not in st.session_state:
    st.session_state["response"] = None

messages = st.session_state.messages
for msg in messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Tell me a joke about sharks"):
    messages.append({"role": "user", "content": prompt})
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
        for m in messages
    ])
    model = GenerativeModel("gemini-2.0-flash-001")
    try:
        response = model.generate_content(history + f"\nUser: {prompt}\nAssistant:")
        st.session_state["response"] = response.text
        with st.chat_message("assistant"):
            messages.append({"role": "assistant", "content": st.session_state["response"]})
            st.write(st.session_state["response"])
    except Exception as e:
        st.error(f"Gemini error: {e}")
        st.stop()

if st.session_state["response"]:
    feedback = streamlit_feedback(
        feedback_type="thumbs",
        optional_text_label="[Optional] Please provide an explanation",
        key=f"feedback_{len(messages)}",
    )
    # This app is logging feedback to Trubrics backend, but you can send it anywhere.
    # The return value of streamlit_feedback() is just a dict.
    # Configure your own account at https://trubrics.streamlit.app/
    if feedback and "TRUBRICS_EMAIL" in st.secrets:
        config = trubrics.init(
            email=st.secrets.TRUBRICS_EMAIL,
            password=st.secrets.TRUBRICS_PASSWORD,
        )
        collection = trubrics.collect(
            component_name="default",
            model="gemini",
            response=feedback,
            metadata={"chat": messages},
        )
        trubrics.save(config, collection)
        st.toast("Feedback recorded!", icon="📝")
