import numpy as np
import pandas as pd
from typing import List, Tuple, Dict

def validate_numeric_input(data: str) -> Tuple[bool, List[float]]:
    """Validate and convert string input to numeric data."""
    try:
        # Split input by commas and convert to float
        numbers = [float(x.strip()) for x in data.split(',')]
        return True, numbers
    except ValueError:
        return False, []

def perform_math_operation(data: List[float], operation: str, value: float) -> List[float]:
    """Perform mathematical operations on the data."""
    if not data:
        raise ValueError("No data provided")
    
    result = []
    try:
        if operation == "Add":
            result = [x + value for x in data]
        elif operation == "Subtract":
            result = [x - value for x in data]
        elif operation == "Multiply":
            result = [x * value for x in data]
        elif operation == "Divide":
            if value == 0:
                raise ValueError("Division by zero is not allowed")
            result = [x / value for x in data]
        return result
    except Exception as e:
        raise ValueError(f"Error performing {operation}: {str(e)}")

def create_dataframe(data: List[float]) -> pd.DataFrame:
    """Create a DataFrame with index numbers."""
    return pd.DataFrame({
        'Index': range(1, len(data) + 1),
        'Value': data
    })

def calculate_statistics(data: List[float]) -> Dict[str, float]:
    """Calculate basic statistics for the data."""
    return {
        'Mean': np.mean(data),
        'Median': np.median(data),
        'Standard Deviation': np.std(data),
        'Minimum': np.min(data),
        'Maximum': np.max(data)
    }
