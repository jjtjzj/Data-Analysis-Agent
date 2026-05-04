import streamlit as st

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
    """Adds a message to the chat history."""
    st.session_state.messages.append({"role": role, "content": content})

def add_log(step, detail):
    """Adds a reasoning step/log to the agent's memory."""
    st.session_state.logs.append({"step": step, "detail": detail})

def clear_logs():
    """Clears the agent reasoning logs."""
    st.session_state.logs = []
