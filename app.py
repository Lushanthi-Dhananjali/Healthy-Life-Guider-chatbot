import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


# 1. Page Setup
st.set_page_config(page_title="Health Guide AI", page_icon="🌿")
st.title("🌿 Healthy Life Guider")
st.caption("Your personal local assistant for fitness, nutrition, and wellness.")

# 2. Define the Persona (The "Modification")
# This is where you define the chatbot's specialized knowledge and behavior.
SYSTEM_PROMPT = """
You are a 'Healthy Life Guider', a professional wellness coach. 

CORE KNOWLEDGE:
- Nutrition, exercise, mental health, and sleep.

STRICT RULES ON TOPIC:
1. ONLY answer questions related to health, fitness, or wellness.
2. If a user asks about UNHEALTHY habits (e.g., 'How can I eat more sugar?'), explain the health risks and suggest a healthy alternative.
3. If a user asks an OFF-TOPIC question (e.g., about movies, cars, politics, or coding), politely say: "I am your Healthy Life Guider. I can only assist you with health and wellness-related topics. Would you like to talk about your fitness goals instead?"
4. NEVER give advice on topics outside of health.

DISCLAIMER:
- Always remind the user you are an AI, not a doctor.
"""

# 3. Initialize Model and Memory
llm = ChatOllama(model="llama3", temperature=0.5)

if "chat_history" not in st.session_state:
    # Start the history with the System Message
    st.session_state.chat_history = [SystemMessage(content=SYSTEM_PROMPT)]

# 4. Display Chat History (Skipping the hidden system message)
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# 5. User Interaction
if user_input := st.chat_input("How can I improve my health today?"):
    # Add user message to history
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Consulting wellness guides..."):
            # Pass the entire history so the AI has context/memory
            response = llm.invoke(st.session_state.chat_history)
            st.markdown(response.content)
            st.session_state.chat_history.append(AIMessage(content=response.content))