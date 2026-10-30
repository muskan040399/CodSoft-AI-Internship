import streamlit as st
import re
import random

# Page Configuration
st.set_page_config(page_title="SmartBot - AI Chatbot Assistant", page_icon="🤖", layout="centered")

# Bot Response Logic
def get_bot_response(user_input):
    text = user_input.lower().strip()
    
    rules = {
        r'\b(hi|hello|hey|greetings|hlw|hy|hiii|hlo)\b': [
            "Hello! Welcome to SmartBot. How can I assist you today?",
            "Hi there! What can I help you with?",
            "Greetings! Ready to assist you."
        ],
        r'\b(how are you|how is it going|how r u|how u doing)\b': [
            "I'm just a bundle of code, but I'm operating smoothly! How about you?",
            "All systems go! How can I help you today?"
        ],
        r'\b(good|fine|great|awesome|im good|i am good|doing well)\b': [
            "Glad to hear that! How can I assist you further?",
            "Awesome! Let me know if you have any questions."
        ],
        r'\b(your name|who are you|who r u)\b': [
            "I am SmartBot, a rule-based AI chatbot designed to help answer your queries.",
            "You can call me SmartBot, your virtual assistant!"
        ],
        r'\b(what can you do|help|assist|support|features)\b': [
            "I can answer common questions, chat casually, and provide quick assistance!",
            "Feel free to greet me, ask about my purpose, or test out my conversational features."
        ],
        r'\b(bye|by|exit|quit|goodbye|see ya|cya)\b': [
            "Goodbye! Have a fantastic day ahead!",
            "Bye! Feel free to drop by whenever you need help again."
        ]
    }
    
    for pattern, responses in rules.items():
        if re.search(pattern, text):
            return random.choice(responses)
            
    fallbacks = [
        "That's interesting! Tell me more.",
        "I'm not quite sure I understand that yet. Could you rephrase?",
        "Hmm, my current rulebook doesn't cover that, but I'm constantly learning!"
    ]
    return random.choice(fallbacks)

# Streamlit UI Design
st.title("🤖 SmartBot - AI Chatbot")
st.caption("🚀 Interactive Rule-Based Chatbot built with Python & Streamlit")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate bot response
    response = get_bot_response(prompt)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)