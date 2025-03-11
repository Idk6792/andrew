import numpy as np
from typing import List, Union, Tuple

def validate_numbers(numbers: List[str]) -> Tuple[bool, List[float], str]:
    """Validate and convert string inputs to numbers."""
    try:
        converted = [float(num.strip()) for num in numbers if num.strip()]
        if not converted:
            return False, [], "Please enter some numbers"
        return True, converted, ""
    except ValueError:
        return False, [], "Please enter valid numbers"

def perform_operation(numbers: List[float], operation: str) -> Tuple[bool, Union[float, List[float]], str]:
    """Perform mathematical operations on the input numbers."""
    try:
        if not numbers:
            return False, 0, "No numbers provided"
            
        if operation == "Sum":
            return True, sum(numbers), ""
        elif operation == "Average":
            return True, np.mean(numbers), ""
        elif operation == "Product":
            return True, np.prod(numbers), ""
        elif operation == "Standard Deviation":
            return True, np.std(numbers), ""
        elif operation == "Cumulative Sum":
            return True, np.cumsum(numbers).tolist(), ""
        else:
            return False, 0, f"Unknown operation: {operation}"
            
    except Exception as e:
        return False, 0, f"Error in calculation: {str(e)}"

def generate_sequence(start: float, end: float, steps: int) -> List[float]:
    """Generate a sequence of numbers."""
    try:
        return list(np.linspace(start, end, steps))
    except Exception:
        return []
