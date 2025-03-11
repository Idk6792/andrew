import streamlit as st
import numpy as np
from utils.math_operations import validate_numbers, perform_operation, generate_sequence
from utils.chart_helpers import (
    create_line_chart,
    create_bar_chart,
    create_scatter_plot,
    apply_chart_styling
)

def initialize_session_state():
    """Initialize session state variables."""
    if 'data_input' not in st.session_state:
        st.session_state.data_input = ""
    if 'operation_result' not in st.session_state:
        st.session_state.operation_result = None
    if 'error_message' not in st.session_state:
        st.session_state.error_message = ""

def main():
    st.set_page_config(
        page_title="Mathematical Chart Maker",
        page_icon="📊",
        layout="wide"
    )

    initialize_session_state()

    st.title("📊 Mathematical Chart Maker")
    st.markdown("---")

    # Create two columns for input and visualization
    input_col, viz_col = st.columns([1, 2])

    with input_col:
        st.subheader("Data Input")
        data_input = st.text_area(
            "Enter numbers (one per line):",
            value=st.session_state.data_input,
            height=150,
            key="data_input_area"
        )

        # Mathematical operations selection
        operation = st.selectbox(
            "Select Operation",
            ["Sum", "Average", "Product", "Standard Deviation", "Cumulative Sum"]
        )

        # Chart type selection
        chart_type = st.selectbox(
            "Select Chart Type",
            ["Line Chart", "Bar Chart", "Scatter Plot"]
        )

        if st.button("Calculate and Plot"):
            # Validate input
            valid, numbers, error = validate_numbers(data_input.split('\n'))
            
            if valid:
                # Perform mathematical operation
                success, result, error = perform_operation(numbers, operation)
                
                if success:
                    st.session_state.operation_result = result
                    st.session_state.error_message = ""
                else:
                    st.session_state.error_message = error
            else:
                st.session_state.error_message = error

    with viz_col:
        # Display error message if any
        if st.session_state.error_message:
            st.error(st.session_state.error_message)
        
        # Display results and charts
        if st.session_state.operation_result is not None:
            st.subheader("Results")
            
            # Display numerical results
            if isinstance(st.session_state.operation_result, (int, float)):
                st.metric(operation, f"{st.session_state.operation_result:.2f}")
            else:
                st.write(f"{operation} result:", st.session_state.operation_result)

            # Generate x-axis values
            x_values = list(range(len(data_input.split('\n'))))
            y_values = [float(num.strip()) for num in data_input.split('\n') if num.strip()]

            # Create appropriate chart
            if chart_type == "Line Chart":
                fig = create_line_chart(x_values, y_values, f"{operation} Visualization")
            elif chart_type == "Bar Chart":
                fig = create_bar_chart(x_values, y_values, f"{operation} Visualization")
            else:  # Scatter Plot
                fig = create_scatter_plot(x_values, y_values, f"{operation} Visualization")

            # Apply styling and display chart
            fig = apply_chart_styling(fig)
            st.plotly_chart(fig, use_container_width=True)

    # Add help section
    with st.expander("Help & Instructions"):
        st.markdown("""
        ### How to use this app:
        1. Enter your numbers in the text area (one number per line)
        2. Select a mathematical operation to perform
        3. Choose a chart type for visualization
        4. Click 'Calculate and Plot' to see the results

        ### Available Operations:
        - **Sum**: Calculates the total of all numbers
        - **Average**: Calculates the mean of the numbers
        - **Product**: Multiplies all numbers together
        - **Standard Deviation**: Calculates the standard deviation
        - **Cumulative Sum**: Shows the running total
        """)

if __name__ == "__main__":
    main()
