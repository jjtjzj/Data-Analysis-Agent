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
model = genai.GenerativeModel('gemini-flash-latest')

SYSTEM_PROMPT = """
You are an expert Data Analyst agent. You have access to a pandas DataFrame named 'df'.
Your goal is to help the user analyze their data by following a structured Reason-Act-Observe loop.

**Format Guidelines:**
1. **Thought**: Explain what you are thinking and why you are taking the next step.
2. **Action**: Provide a Python code block starting with ```python. Use `print()` to output results.
3. **Observation**: This will be the result of your code execution (provided to you in the next step).
4. **Final Answer**: Once you have the necessary information, provide a clear summary answer.

**Important**: 
- Only provide ONE Thought and ONE Action (code block) at a time.
- If no more analysis is needed, skip the Action and provide the Final Answer.
- Always use `print()` for any values you want to see in the Observation.
"""

def run_agent_loop(user_prompt, df):
    """
    Executes the ReAct loop:
    1. Generates Thought + Action.
    2. Executes Action (tools.py) to get Observation.
    3. Repeats or provides Final Answer.
    """
    memory.clear_logs()
    
    # Prepare context
    df_info = f"Columns: {list(df.columns)}\nData Types:\n{df.dtypes}\nShape: {df.shape}"
    conversation_context = f"User Question: {user_prompt}\n\nDataframe Context:\n{df_info}"
    
    memory.add_log("System", "Analyzing request...")
    
    try:
        # Step 1: Reason and Act
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\n{conversation_context}")
        response_text = response.text
        
        # Parse Thought
        thought = "No thought provided."
        if "Thought:" in response_text:
            thought = response_text.split("Thought:")[1].split("Action:")[0].split("```")[0].strip()
        memory.add_log("Thought", thought)
        
        # Check for Code Action
        if "```python" in response_text:
            code = response_text.split("```python")[1].split("```")[0].strip()
            memory.add_log("Action (Code)", f"```python\n{code}\n```")
            
            # Step 2: Execute and Observe
            observation = tools.execute_python_code(code, df)
            memory.add_log("Observation", observation)
            
            # Step 3: Final Synthesis
            final_prompt = f"{SYSTEM_PROMPT}\n\n{conversation_context}\n\nPrevious Reasoning: {thought}\nCode Executed:\n{code}\nObservation: {observation}\n\nPlease provide your Final Answer."
            final_response = model.generate_content(final_prompt)
            return final_response.text
        else:
            # If no code was generated, treat the response as the final answer or extract it
            if "Final Answer:" in response_text:
                return response_text.split("Final Answer:")[1].strip()
            return response_text
            
    except Exception as e:
        error_msg = f"Error in agent loop: {e}"
        memory.add_log("Error", error_msg)
        return error_msg
