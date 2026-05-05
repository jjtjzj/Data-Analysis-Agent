import pandas as pd
import io
import contextlib
import matplotlib.pyplot as plt

def execute_python_code(code, df):
    """
    Executes Python code in a restricted environment and returns the output.
    """
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        try:
            # Create a restricted global namespace
            # We remove __builtins__ to prevent access to functions like open, eval, etc.
            # Then we selectively add back safe ones if needed, or just let them fail.
            restricted_globals = {
                "__builtins__": {
                    "print": print,
                    "range": range,
                    "len": len,
                    "list": list,
                    "dict": dict,
                    "str": str,
                    "int": int,
                    "float": float,
                    "sum": sum,
                    "min": min,
                    "max": max,
                    "round": round,
                },
                "pd": pd,
                "plt": plt,
                "df": df
            }
            
            # Execute the code
            exec(code, restricted_globals)
            
            result = output.getvalue()
            return result if result else "Code executed successfully."
        except Exception as e:
            return f"Error during execution: {e}"
