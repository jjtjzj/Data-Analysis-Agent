import streamlit as st
import pandas as pd
import memory
import agent
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Agentic Data Analyst", layout="wide", page_icon="🤖")

def main():
    # Initialize session state
    memory.init_memory()
    if "plot_generated" not in st.session_state:
        st.session_state.plot_generated = False
    
    # --- Custom CSS for Premium Look ---
    st.markdown("""
        <style>
        /* Main Title */
        .main-title {
            font-size: 2.5rem;
            font-weight: 700;
            color: #6F42C1;
            margin-bottom: 0.5rem;
        }
        /* Chat Bubbles */
        .stChatMessage {
            padding: 1.2rem;
            border-radius: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        /* User Message (Coral) */
        [data-testid="stChatMessage"][aria-label="Chat message from user"] {
            background-color: rgba(255, 127, 80, 0.05);
            border-right: 5px solid #FF7F50;
        }
        /* Assistant Message (Purple) */
        [data-testid="stChatMessage"][aria-label="Chat message from assistant"] {
            background-color: rgba(111, 66, 193, 0.05);
            border-left: 5px solid #6F42C1;
        }
        /* Timestamp Style */
        .chat-timestamp {
            font-size: 0.7rem;
            color: #aaa;
            margin-top: 8px;
            font-style: italic;
        }
        /* Reasoning Container */
        .reasoning-container {
            border: 1px solid rgba(111, 66, 193, 0.2);
            border-radius: 10px;
            padding: 15px;
            background-color: #fcfaff;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-title">🤖 Agentic Data Analyst</h1>', unsafe_allow_html=True)
    st.caption("Expert Data Analysis Agent powered by Gemini & Pandas")
    st.markdown("---")

    # --- Sidebar: Data & Controls ---
    with st.sidebar:
        st.header("📂 Data Source")
        uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.df = df
                
                st.success("Dataset loaded successfully!")
                
                # Enhanced Metrics
                st.markdown("### 📊 Dataset Overview")
                m1, m2 = st.columns(2)
                m1.metric("Rows", df.shape[0])
                m2.metric("Columns", df.shape[1])
                
                m3, m4 = st.columns(2)
                m3.metric("Missing Values", df.isnull().sum().sum())
                m4.metric("Memory", f"{df.memory_usage().sum() / 1024**2:.2f} MB")
                
                with st.expander("🔍 Interactive Preview"):
                    st.dataframe(df.head(10), use_container_width=True)
                
                with st.expander("📑 Column Information"):
                    st.write(df.dtypes)
                
                # Download
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Dataset",
                    data=csv,
                    file_name=f"processed_{uploaded_file.name}",
                    mime='text/csv',
                    use_container_width=True
                )
                    
            except Exception as e:
                st.error(f"Error: {e}")
        
        st.markdown("---")
        if st.button("🗑️ Reset Conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.logs = []
            st.session_state.plot_generated = False
            st.rerun()

    # --- Main Layout: Two Columns ---
    col_chat, col_logs = st.columns([1.8, 1.2], gap="large")

    # --- Left Column: Chat ---
    with col_chat:
        st.subheader("💬 Conversation")
        
        # History Management: Collapse older messages
        if len(st.session_state.messages) > 6:
            with st.expander(f"📜 View {len(st.session_state.messages) - 6} older messages", expanded=False):
                for message in st.session_state.messages[:-6]:
                    avatar = "👤" if message["role"] == "user" else "🤖"
                    with st.chat_message(message["role"], avatar=avatar):
                        st.markdown(message["content"])
                        st.markdown(f'<div class="chat-timestamp">{message.get("timestamp", "")}</div>', unsafe_allow_html=True)

        # Recent messages
        for message in st.session_state.messages[-6:]:
            avatar = "👤" if message["role"] == "user" else "🤖"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
                st.markdown(f'<div class="chat-timestamp">{message.get("timestamp", "")}</div>', unsafe_allow_html=True)
        
        # Chat input at the bottom
        if prompt := st.chat_input("Ask a question about your data..."):
            if st.session_state.df is None:
                st.warning("Please upload a CSV file first.")
            else:
                # Add to history
                memory.add_message("user", prompt)
                st.rerun() # Rerun to show the user message immediately

        # Processing logic (if the last message is from user)
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            last_prompt = st.session_state.messages[-1]["content"]
            with st.chat_message("assistant", avatar="🤖"):
                with st.status("🚀 Agent is processing...", expanded=True) as status:
                    st.write("Initializing reasoning loop...")
                    response = agent.run_agent_loop(last_prompt, st.session_state.df)
                    status.update(label="Analysis complete!", state="complete", expanded=False)
                
                st.markdown(response)
                
                if st.session_state.get("plot_generated"):
                    st.image("plot.png", caption="Visual Insight", use_container_width=True)
                
                memory.add_message("assistant", response)
                st.rerun()

    # --- Right Column: Reasoning ---
    with col_logs:
        st.subheader("🧠 Agent Reasoning")
        if not st.session_state.logs:
            st.info("The agent's thought process will appear here.")
        
        for log in st.session_state.logs:
            step_title = log['step'].lower()
            
            # Status Badges & Icons
            icon = "💡"
            if "thought" in step_title: icon = "💡"
            elif "action" in step_title: icon = "⚙️"
            elif "observation" in step_title: icon = "🔍"
            elif "system" in step_title: icon = "🛠️"
            
            status_icon = "✅"
            if "error" in step_title: 
                status_icon = "❌"
                icon = "⚠️"
            elif "attempt" in step_title: 
                status_icon = "🔄"
            
            # Rendering in a styled container
            with st.container(border=True):
                c1, c2 = st.columns([0.15, 0.85])
                with c1:
                    st.markdown(f"### {icon}")
                with c2:
                    st.markdown(f"**{log['step']}** {status_icon}")
                    st.caption(f"Time: {log.get('timestamp', '')}")
                    
                    if "error" in step_title:
                        st.error(log['detail'])
                    elif "action" in step_title:
                        st.code(log['detail'], language="python")
                    else:
                        st.markdown(log['detail'])

if __name__ == "__main__":
    main()
