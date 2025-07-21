import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash-8b")

# Streamlit UI setup
st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("My Chat bot")
st.write("How can i assist hep you?")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("You:", placeholder="Write your query here....", key="input")

# Chat logic
if user_input:
    with st.spinner("Thinking..."):
        try:
            response = model.generate_content(user_input)
            bot_reply = response.text.strip()

            # Save to session state chat history
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", bot_reply))

        except Exception as e:
            st.error(f"Error: {str(e)}")


# Display chat history
for speaker, message in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")



                                         


 

