import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()
MODEL = "gemini-3.5-flash-lite"  # use the model name that worked for you

st.title("📚 Ask the Docs")

# Runs only once, the first time the page opens
if "chat" not in st.session_state:
    st.session_state.client = genai.Client()
    st.session_state.chat = st.session_state.client.chats.create(model=MODEL)
    st.session_state.messages = []

# Show all previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Wait for the user to type something
prompt = st.chat_input("Ask me anything...")

if prompt:
    # Show and save the user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and show the bot's answer
    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(prompt)
            answer = response.text
        except errors.ServerError:
            answer = "The model is busy right now. Please try again in a moment."
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})