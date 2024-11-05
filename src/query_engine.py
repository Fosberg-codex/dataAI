import pandas as pd
from typing import Any

class QueryEngine:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def process_query(self, df: pd.DataFrame, question: str) -> str:
        # Prepare data context
        data_context = self._prepare_data_context(df)
        
        # Construct prompt
        prompt = f"""
Given the following dataset information:

{data_context}

Question: {question}

Please analyze the data and provide a clear, detailed answer. Include relevant statistics or calculations if appropriate.
"""
        
        # Get response from API
        return self.api_client.analyze(prompt)

    def _prepare_data_context(self, df: pd.DataFrame) -> str:
        # Prepare a summary of the dataset
        context = f"""
Dataset Summary:
- Total rows: {len(df)}
- Columns: {', '.join(df.columns)}
- Sample data (first 5 rows):
{df.head().to_string()}

Column Information:
"""
        
        # Add information about each column
        for col in df.columns:
            dtype = df[col].dtype
            n_unique = df[col].nunique()
            n_missing = df[col].isna().sum()
            
            context += f"\n{col}:"
            context += f"\n  - Type: {dtype}"
            context += f"\n  - Unique values: {n_unique}"
            context += f"\n  - Missing values: {n_missing}"
            
            if pd.api.types.is_numeric_dtype(df[col]):
                context += f"\n  - Min: {df[col].min()}"
                context += f"\n  - Max: {df[col].max()}"
                context += f"\n  - Mean: {df[col].mean()}"
        
        return context
