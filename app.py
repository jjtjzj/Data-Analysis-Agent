import streamlit as st
import pandas as pd
import memory
import agent
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Agentic Data Analyst", layout="wide")

def main():
    # Initialize session state
    memory.init_memory()
    
    st.title("🤖 Agentic Data Analyst")
    
    # --- Custom CSS for Premium Look ---
    st.markdown("""
        <style>
        /* Chat Bubbles */
        .stChatMessage {
            padding: 1rem;
            border-radius: 15px;
            margin-bottom: 10px;
        }
        /* User Message (Coral/Red) */
        [data-testid="stChatMessage"][aria-label="Chat message from user"] {
            background-color: rgba(255, 127, 80, 0.1);
            border-left: 5px solid #FF7F50;
        }
        /* Assistant Message (Orange/Yellow) */
        [data-testid="stChatMessage"][aria-label="Chat message from assistant"] {
            background-color: rgba(255, 165, 0, 0.1);
            border-left: 5px solid #FFA500;
        }
        /* Timestamp Style */
        .chat-timestamp {
            font-size: 0.75rem;
            color: #888;
            margin-top: 5px;
            text-align: right;
        }
        /* Reasoning Expander */
        .stExpander {
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 8px;
            background-color: rgba(128, 128, 128, 0.05);
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    # --- Sidebar: Data Upload ---
    with st.sidebar:
        st.header("📂 Data Source")
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.df = df
                
                # Quick Stats
                st.success("File uploaded!")
                col1, col2 = st.columns(2)
                col1.metric("Rows", df.shape[0])
                col2.metric("Cols", df.shape[1])
                
                st.write("### Data Preview")
                st.dataframe(df.head(10), use_container_width=True)
                
                # Download Button
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Full Data",
                    data=csv,
                    file_name=uploaded_file.name,
                    mime='text/csv',
                )
                
                # Data Types Info
                with st.expander("📊 Column Types"):
                    st.write(df.dtypes)
                    
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
        
        st.markdown("---")
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.session_state.logs = []
            st.rerun()

    # --- Main Layout: Two Columns ---
    col_chat, col_logs = st.columns([3, 2])

    # --- Left Column: Chat History ---
    with col_chat:
        st.header("💬 Chat")
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                st.markdown(f'<div class="chat-timestamp">{message.get("timestamp", "")}</div>', unsafe_allow_html=True)
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your data..."):
            if st.session_state.df is None:
                st.warning("Please upload a CSV file first.")
            else:
                # Add user message to memory
                memory.add_message("user", prompt)
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Assistant response
                with st.chat_message("assistant"):
                    with st.spinner("Agent is thinking..."):
                        response = agent.run_agent_loop(prompt, st.session_state.df)
                        st.markdown(response)
                        memory.add_message("assistant", response)
                
                # Rerun to update logs in the right column
                st.rerun()

    # --- Right Column: Transparency (Reasoning Logs) ---
    with col_logs:
        st.header("🧠 Agent Reasoning")
        if not st.session_state.logs:
            st.info("Reasoning steps will appear here during processing.")
        
        for log in st.session_state.logs:
            # Choose icon based on step type
            step = log['step'].lower()
            icon = "💡" if "thought" in step or "reasoning" in step else "⚙️" if "action" in step else "🔍" if "observation" in step else "📝"
            
            with st.expander(f"{icon} {log['step']} ({log.get('timestamp', '')})", expanded=True):
                st.markdown(log['detail'])

if __name__ == "__main__":
    main()
