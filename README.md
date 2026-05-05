# 🤖 Agentic Data Analyst

An advanced, university-level Custom Data Analysis Agent designed to demonstrate agentic behavior through reasoning, tool-use, observation, and autonomous self-correction. Built with **Streamlit**, **Google Gemini**, and **Pandas**.

## 🌟 Key Features

*   **🧠 ReAct Reasoning Loop**: Follows a strict *Thought → Action → Observation* pattern for full transparency.
*   **🛠️ Secure Code Sandbox**: Executes LLM-generated Python code in a restricted environment to ensure safety.
*   **🔄 Autonomous Self-Correction**: Automatically detects execution errors, analyzes tracebacks, and rewrites code (up to 5 attempts).
*   **📊 Dynamic Visualization**: Intercepts matplotlib commands to generate and display real-time data charts.
*   **🔍 High Transparency**: Dedicated reasoning panel showing the agent's internal thought process and generated code.
*   **📈 Dataset Insights**: Real-time metrics including row/column counts, memory usage, and missing value detection.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- A Google Gemini API Key ([Get one here](https://ai.google.dev/))

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/jjtjzj/Data-Analysis-Agent.git
    cd Data-Analysis-Agent
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    Create a `.env` file in the root directory and add your Gemini API key:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

### Running the Application

Start the Streamlit dashboard:
```bash
streamlit run app.py
```
Or use the provided batch file (Windows):
```bash
run_app.bat
```

---

## 📖 Usage Walkthrough

1.  **Upload Data**: Drag and drop any CSV file into the sidebar.
2.  **Inspect Dataset**: Review the interactive data preview and column metrics.
3.  **Ask Questions**: Use the chat interface to ask complex questions like:
    *   *"What is the average salary by department?"*
    *   *"Can you plot a histogram of employee ages?"*
    *   *"Find the top 5 highest earners and show their details."*
4.  **Monitor Reasoning**: Watch the **Agent Reasoning** panel on the right to see how the agent breaks down your request, handles errors, and arrives at the answer.

---

## 📂 Project Structure

- `app.py`: Main Streamlit UI and layout logic.
- `agent.py`: Core ReAct loop, LLM integration, and self-correction logic.
- `tools.py`: Secure Python execution sandbox and plot interception.
- `memory.py`: Session state management for chat history and reasoning logs.
- `.streamlit/config.toml`: Custom branding and theme settings.

---

## 🎓 Academic Context
This project was developed for **COMPSCI 767 - Intelligent Software Agents**. It demonstrates the implementation of a goal-oriented agent capable of using tools to interact with its environment (data) and correcting its behavior based on feedback.
