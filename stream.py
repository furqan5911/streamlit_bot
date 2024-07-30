import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Configuring Streamlit page settings
st.set_page_config(
    page_title="GPT-4 Chat",
    page_icon="💬",
    layout="centered"
)

# Initialize chat session in Streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit page title
st.title("🤖 Accountability ChatBot")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input("Ask GPT-4...")

if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Define the detailed task for the assistant
    detailed_task = (
        "You have to give 5 questions for each enabler based on the indicator. "
        "The enablers are Emotional Management, Limiting Beliefs Management, Self-Awareness, Mindfulness, Biased-Free Behavior. "
        "The indicators are Emotional Awareness, Stress Management, Resilience, Positive Action, Emotional Regulation, Belief Identification, "
        "Thought Monitoring, Reframing, Self-Talk, Proactive Prevention, Values Identification, Needs and Wants, Strengths and Weaknesses, "
        "Self-Esteem Alignment, Reflective Practice, Present Moment Awareness, Body Awareness, Thought Observation, Emotional Awareness, "
        "Non-Judgmental Attitude, Inclusivity, Cultural Competence, Open-Mindedness, Ego Management, Respectful Communication. "
        "The response should be in the form of a question. For example, if the enabler is Emotional Management and the indicator is Emotional Awareness, "
        "the question could be 'How do you manage your emotions?' Try to give an answer for each of the sub-enabler with its respective question "
        "and try to give response in context of user prompt {user_prompt}."
    )

    # Concatenate the detailed task with the user prompt
    full_prompt = detailed_task.replace("{user_prompt}", user_prompt)

    # Add the full prompt to the chat history for context
    st.session_state.chat_history.append({"role": "user", "content": full_prompt})

    # Send the full prompt to GPT-4 and get a response
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful Accountability assistant"},
            *st.session_state.chat_history
        ]
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Display GPT-4's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    # Remove the full prompt from chat history to only show the user prompt
    st.session_state.chat_history.pop(-2)
