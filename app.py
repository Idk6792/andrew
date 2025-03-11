import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    validate_numeric_input,
    perform_math_operation,
    create_dataframe,
    calculate_statistics
)

def initialize_session_state():
    """Initialize session state variables."""
    if 'data' not in st.session_state:
        st.session_state.data = []
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = []

def render_header():
    """Render the application header."""
    st.title("Mathematical Chart Maker")
    st.markdown("""
    Enter comma-separated numbers, perform mathematical operations, 
    and visualize the results through different chart types.
    """)

def render_data_input():
    """Render the data input section."""
    st.header("Data Input")
    data_input = st.text_area(
        "Enter your numbers (comma-separated):",
        placeholder="Example: 1.5, 2.0, 3.5, 4.0"
    )
    
    if st.button("Process Data"):
        if data_input:
            is_valid, numbers = validate_numeric_input(data_input)
            if is_valid:
                st.session_state.data = numbers
                st.session_state.processed_data = numbers.copy()
                st.success("Data processed successfully!")
            else:
                st.error("Please enter valid numeric values separated by commas.")
        else:
            st.error("Please enter some data.")

def render_math_operations():
    """Render the mathematical operations section."""
    if st.session_state.data:
        st.header("Mathematical Operations")
        col1, col2 = st.columns(2)
        
        with col1:
            operation = st.selectbox(
                "Select Operation",
                ["Add", "Subtract", "Multiply", "Divide"]
            )
        
        with col2:
            value = st.number_input("Enter Value", value=0.0)
        
        if st.button("Apply Operation"):
            try:
                st.session_state.processed_data = perform_math_operation(
                    st.session_state.data,
                    operation,
                    value
                )
                st.success(f"Operation {operation} completed successfully!")
            except ValueError as e:
                st.error(str(e))

def render_statistics():
    """Render the statistics section."""
    if st.session_state.processed_data:
        st.header("Statistics")
        stats = calculate_statistics(st.session_state.processed_data)
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Mean", f"{stats['Mean']:.2f}")
            st.metric("Median", f"{stats['Median']:.2f}")
            st.metric("Standard Deviation", f"{stats['Standard Deviation']:.2f}")
        
        with col2:
            st.metric("Minimum", f"{stats['Minimum']:.2f}")
            st.metric("Maximum", f"{stats['Maximum']:.2f}")

def render_charts():
    """Render the charts section."""
    if st.session_state.processed_data:
        st.header("Data Visualization")
        
        chart_type = st.selectbox(
            "Select Chart Type",
            ["Line Chart", "Bar Chart", "Scatter Plot"]
        )
        
        df = create_dataframe(st.session_state.processed_data)
        
        if chart_type == "Line Chart":
            fig = px.line(
                df,
                x='Index',
                y='Value',
                title='Line Chart of Values',
                markers=True
            )
        elif chart_type == "Bar Chart":
            fig = px.bar(
                df,
                x='Index',
                y='Value',
                title='Bar Chart of Values'
            )
        else:  # Scatter Plot
            fig = px.scatter(
                df,
                x='Index',
                y='Value',
                title='Scatter Plot of Values'
            )
        
        fig.update_layout(
            xaxis_title="Data Point Index",
            yaxis_title="Value",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

def main():
    """Main application function."""
    initialize_session_state()
    render_header()
    render_data_input()
    render_math_operations()
    render_statistics()
    render_charts()

if __name__ == "__main__":
    main()
