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

# Define enablers and their corresponding indicators
enablers = {
    "Emotional Management": ["Emotional Awareness", "Stress Management", "Resilience", "Positive Action", "Emotional Regulation"],
    "Limiting Beliefs Management": ["Belief Identification", "Thought Monitoring", "Reframing", "Self-Talk", "Proactive Prevention"],
    "Self-Awareness": ["Values Identification", "Needs and Wants", "Strengths and Weaknesses", "Self-Esteem Alignment", "Reflective Practice"],
    "Mindfulness": ["Present Moment Awareness", "Body Awareness", "Thought Observation", "Emotional Awareness", "Non-Judgmental Attitude"],
    "Biased-Free Behavior": ["Inclusivity", "Cultural Competence", "Open-Mindedness", "Ego Management", "Respectful Communication"]
}

# Sidebar dropdown menu for enabler selection
selected_enabler = st.sidebar.selectbox("Select an enabler", list(enablers.keys()))

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

    # Define the detailed task for the assistant based on the selected enabler
    indicators = ", ".join(enablers[selected_enabler])
    detailed_task = (
        f"You are only allowed to respond to queries related to the enabler '{selected_enabler}'. "
        f"The indicators for this enabler are {indicators}. "
        "If the user's query is not related to this enabler, you should politely decline to answer. "
        f"and try to give response in context of user prompt: {user_prompt}.if it is not related to the enabler '{selected_enabler}', you should politely decline to answer."
    )

    # Concatenate the detailed task with the user prompt
    full_prompt = detailed_task

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

   
