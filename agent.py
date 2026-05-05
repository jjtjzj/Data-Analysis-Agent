import os
import google.generativeai as genai
from dotenv import load_dotenv
import memory
import tools
import streamlit as st

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("Warning: GEMINI_API_KEY not found in environment.")

# Initialize the model
# Switching to gemini-1.5-flash-latest to avoid 429 quota issues on experimental models
model = genai.GenerativeModel('gemini-1.5-flash-latest')

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
- For plots, use `plt.show()` or just create the plot; the system will capture it automatically.
"""

def run_agent_loop(user_prompt, df):
    """
    Executes the ReAct loop with Self-Correction:
    1. Generates Thought + Action.
    2. Executes Action (tools.py) to get Observation and Plot flag.
    3. If Error, provides feedback to LLM and retries (Max 5).
    4. Synthesizes Final Answer.
    """
    memory.clear_logs()
    st.session_state.plot_generated = False # Reset plot flag
    
    # Prepare context
    df_info = f"Columns: {list(df.columns)}\nData Types:\n{df.dtypes}\nShape: {df.shape}"
    conversation_context = f"User Question: {user_prompt}\n\nDataframe Context:\n{df_info}"
    
    memory.add_log("System", "Analyzing request...")
    
    max_attempts = 5
    attempt = 0
    current_prompt = f"{SYSTEM_PROMPT}\n\n{conversation_context}"
    
    try:
        while attempt < max_attempts:
            attempt += 1
            response = model.generate_content(current_prompt)
            response_text = response.text
            
            # Parse Thought
            thought = "No thought provided."
            if "Thought:" in response_text:
                thought = response_text.split("Thought:")[1].split("Action:")[0].split("```")[0].strip()
            
            log_prefix = f"Attempt {attempt}: " if attempt > 1 else ""
            memory.add_log(f"{log_prefix}Thought", thought)
            
            # Check for Code Action
            if "```python" in response_text:
                code = response_text.split("```python")[1].split("```")[0].strip()
                memory.add_log(f"{log_prefix}Action (Code)", f"```python\n{code}\n```")
                
                # Step 2: Execute and Observe
                exec_result = tools.execute_python_code(code, df)
                observation = exec_result["output"]
                
                if "Error during execution" in observation:
                    memory.add_log(f"{log_prefix}Observation (Error)", observation)
                    # Update prompt for self-correction
                    current_prompt += f"\n\nPrevious Code Attempt:\n{code}\n\nError Received:\n{observation}\n\n**Task**: Analyze the error and provide a corrected Thought and Action (code)."
                    continue # Retry
                else:
                    memory.add_log(f"{log_prefix}Observation", observation)
                    
                    # Capture plot generation
                    if exec_result.get("plot_generated"):
                        st.session_state.plot_generated = True
                        memory.add_log("System", "Visual chart generated! 📊")

                    # Success! Now synthesize final answer
                    final_prompt = f"{SYSTEM_PROMPT}\n\n{conversation_context}\n\nFinal Observation: {observation}\n\nPlease provide your Final Answer."
                    final_response = model.generate_content(final_prompt)
                    return final_response.text
            else:
                # If no code was generated, treat as final answer
                if "Final Answer:" in response_text:
                    return response_text.split("Final Answer:")[1].strip()
                return response_text
        
        return "Agent reached maximum self-correction attempts without success."
            
    except Exception as e:
        error_msg = f"Error in agent loop: {e}"
        memory.add_log("Error", error_msg)
        return error_msg
