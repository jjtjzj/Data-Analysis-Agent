import pandas as pd
import io
import contextlib
import matplotlib.pyplot as plt

def execute_python_code(code, df):
    """
    Executes Python code in a restricted environment, intercepts plots, and returns the results.
    """
    # Clear any previous plots to ensure we only capture the new one
    plt.clf()
    
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        try:
            # Create a restricted global namespace
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
            
            # Check if a plot was generated
            plot_generated = False
            if plt.gcf().get_axes():
                plt.savefig("plot.png")
                plot_generated = True
            
            result = output.getvalue()
            return {
                "output": result if result else "Code executed successfully.",
                "plot_generated": plot_generated
            }
        except Exception as e:
            return {
                "output": f"Error during execution: {e}",
                "plot_generated": False
            }
