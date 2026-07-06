import os
import pandas as pd

# Abstraction layer for GPU acceleration
try:
    import cudf
    USE_CUDF = True
except ImportError:
    USE_CUDF = False

def load_data(file_path):
    """Loads data using cudf if available, else pandas."""
    if USE_CUDF:
        try:
            print("Using NVIDIA RAPIDS cuDF for data loading.")
            return cudf.read_csv(file_path)
        except Exception as e:
            print(f"cuDF failed, falling back to pandas: {e}")
            return pd.read_csv(file_path)
    else:
        print("Using pandas for data loading.")
        return pd.read_csv(file_path)

def to_pandas(df):
    """Converts dataframe to pandas if it is a cudf dataframe."""
    if USE_CUDF and isinstance(df, cudf.DataFrame):
        return df.to_pandas()
    return df
