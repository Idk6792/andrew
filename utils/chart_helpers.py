import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import List, Dict, Any

def create_line_chart(x_data: List[float], y_data: List[float], title: str) -> go.Figure:
    """Create a line chart using Plotly."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers', name='Data'))
    fig.update_layout(
        title=title,
        xaxis_title="X Values",
        yaxis_title="Y Values",
        template="plotly_white"
    )
    return fig

def create_bar_chart(x_data: List[float], y_data: List[float], title: str) -> go.Figure:
    """Create a bar chart using Plotly."""
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x_data, y=y_data, name='Data'))
    fig.update_layout(
        title=title,
        xaxis_title="X Values",
        yaxis_title="Y Values",
        template="plotly_white"
    )
    return fig

def create_scatter_plot(x_data: List[float], y_data: List[float], title: str) -> go.Figure:
    """Create a scatter plot using Plotly."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='markers', name='Data'))
    fig.update_layout(
        title=title,
        xaxis_title="X Values",
        yaxis_title="Y Values",
        template="plotly_white"
    )
    return fig

def apply_chart_styling(fig: go.Figure) -> go.Figure:
    """Apply consistent styling to charts."""
    fig.update_layout(
        font=dict(family="Arial", size=12),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    return fig
