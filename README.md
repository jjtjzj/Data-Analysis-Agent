# Data Analysis Agent

A university-level Custom Data Analysis Agent built with Streamlit and Google Gemini.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Add your Gemini API key to `.env` file (e.g. `GEMINI_API_KEY=your_key`)
3. Run the app: `streamlit run app.py`

## Architecture
This agent implements a ReAct loop:
1. **Reason**: The LLM reasons about the user's question and the data schema.
2. **Act**: The LLM generates Python code, which is executed locally.
3. **Observe**: The execution output or errors are observed.
4. **Improve (Self-Correction)**: If an error occurs, the agent corrects its code and retries (up to 5 times).
