import os
import google.generativeai as genai
from dotenv import load_dotenv
import memory
import tools

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("Warning: GEMINI_API_KEY not found in environment.")

# Initialize the model
model = genai.GenerativeModel('gemini-2.0-flash')

SYSTEM_PROMPT = """
You are an expert Data Analyst agent. You have access to a pandas DataFrame named 'df'.
Your goal is to help the user analyze their data by writing and executing Python code.

Guidelines:
1. **Reasoning**: Always start by explaining what you are going to do.
2. **Code**: If analysis is needed, provide Python code. Use `print()` to display results.
3. **Format**: Use the following structure:
   Thought: <your reasoning>
   Code: 
   ```python
   # your code here
   ```
"""

def run_agent_loop(user_prompt, df):
    """
    Executes a basic agent reasoning loop.
    1. Generates reasoning and code.
    2. Executes the code.
    3. Provides a final answer based on results.
    """
    memory.clear_logs()
    
    # Prepare context
    df_info = f"Columns: {list(df.columns)}\nData Types:\n{df.dtypes}\nShape: {df.shape}"
    full_prompt = f"{SYSTEM_PROMPT}\n\nDataframe Context:\n{df_info}\n\nUser Question: {user_prompt}"
    
    memory.add_log("System", "Sending request to Gemini...")
    
    try:
        # Step 1: Initial Reasoning & Code Generation
        response = model.generate_content(full_prompt)
        response_text = response.text
        
        # Parse Thought and Code
        thought = ""
        if "Thought:" in response_text:
            thought = response_text.split("Thought:")[1].split("Code:")[0].strip()
        else:
            thought = response_text # Fallback
            
        memory.add_log("Reasoning", thought)
        
        # Check for code block
        if "```python" in response_text:
            code = response_text.split("```python")[1].split("```")[0].strip()
            memory.add_log("Action", f"Executing analysis code...")
            
            # Step 2: Execution
            observation = tools.execute_python_code(code, df)
            memory.add_log("Observation", observation)
            
            # Step 3: Final Answer
            final_prompt = f"{full_prompt}\n\nPrevious Output:\n{response_text}\n\nObservation from code execution:\n{observation}\n\nPlease provide a final summary answer to the user."
            final_response = model.generate_content(final_prompt)
            return final_response.text
        else:
            return response_text
            
    except Exception as e:
        error_msg = f"Error in agent loop: {e}"
        memory.add_log("Error", error_msg)
        return error_msg
