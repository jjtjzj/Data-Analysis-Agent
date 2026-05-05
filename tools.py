import pandas as pd
import io
import contextlib
import matplotlib.pyplot as plt

def execute_python_code(code, df):
    """
    Executes Python code and returns the output.
    The code has access to the dataframe 'df' and pandas 'pd'.
    """
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        try:
            # Create a local namespace
            local_vars = {"df": df, "pd": pd, "plt": plt}
            exec(code, {}, local_vars)
            
            result = output.getvalue()
            return result if result else "Code executed successfully."
        except Exception as e:
            return f"Error: {e}"
