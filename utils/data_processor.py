import pandas as pd
from utils.data_loader import to_pandas

def process_data(df):
    """
    Preprocesses the data: handles missing values, removes duplicates, 
    and engineers features.
    """
    df = to_pandas(df)
    
    # Drop duplicates
    df = df.drop_duplicates()
    
    # Handle missing values - simple imputation for numeric
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    
    # Feature engineering
    if all(c in df.columns for c in ['Mid_Exam', 'Final_Exam']):
        df['Exam_Trend'] = df['Final_Exam'] - df['Mid_Exam']
        
    return df
