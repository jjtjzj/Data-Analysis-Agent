import streamlit as st
from datetime import datetime

def init_memory():
    """Initializes the Streamlit session state variables for memory and state management."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "logs" not in st.session_state:
        st.session_state.logs = []
        
    if "df" not in st.session_state:
        st.session_state.df = None

    if "current_plot" not in st.session_state:
        st.session_state.current_plot = None

def add_message(role, content):
    """Adds a message to the chat history with a timestamp."""
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": role, 
        "content": content, 
        "timestamp": timestamp
    })

def add_log(step, detail):
    """Adds a reasoning step/log to the agent's memory with a timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append({
        "step": step, 
        "detail": detail, 
        "timestamp": timestamp
    })

def clear_logs():
    """Clears the agent reasoning logs."""
    st.session_state.logs = []
