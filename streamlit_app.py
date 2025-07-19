# chatbot_app.py

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")

# Input your OpenAI API Key
api_key = st.text_input("Enter your OpenAI API Key", type="password")

if api_key:
    client = OpenAI(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show past messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    if prompt := st.chat_input("Say something..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Call OpenAI API
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
                stream=True
            )
            response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("Please enter your OpenAI API key to start chatting.")
