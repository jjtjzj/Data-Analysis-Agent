import streamlit as st
import pandas as pd
import memory

# Page configuration
st.set_page_config(page_title="Agentic Data Analyst", layout="wide")

def main():
    # Initialize session state
    memory.init_memory()
    
    st.title("🤖 Agentic Data Analyst")
    st.markdown("---")

    # --- Sidebar: Data Upload ---
    with st.sidebar:
        st.header("📂 Data Source")
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.df = df
                st.success("File uploaded successfully!")
                st.write("### Data Preview")
                st.dataframe(df.head(5))
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
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your data..."):
            if st.session_state.df is None:
                st.warning("Please upload a CSV file first.")
            else:
                # Add user message to memory
                memory.add_message("user", prompt)
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Placeholder for assistant response (Phase 3+)
                with st.chat_message("assistant"):
                    st.info("Agent logic will be implemented in Phase 3.")

    # --- Right Column: Transparency (Reasoning Logs) ---
    with col_logs:
        st.header("🧠 Agent Reasoning")
        if not st.session_state.logs:
            st.info("Reasoning steps will appear here during processing.")
        
        for log in st.session_state.logs:
            with st.expander(f"Step: {log['step']}", expanded=True):
                st.markdown(log['detail'])

if __name__ == "__main__":
    main()
