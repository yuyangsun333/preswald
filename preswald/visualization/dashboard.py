from plotly.subplots import make_subplots
import plotly.graph_objects as go

def create_dashboard(charts, layout=None, title="Dashboard"):
    """
    Create a dashboard by combining multiple charts.

    Args:
        charts (list): List of plotly figures to include in the dashboard.
        layout (tuple): Tuple specifying rows and columns for layout (default: single column).
        title (str): Title of the dashboard.

    Returns:
        plotly.graph_objects.Figure: The dashboard figure.
    """
    if not layout:
        layout = (len(charts), 1)  # Default: one chart per row

    rows, cols = layout
    fig = make_subplots(rows=rows, cols=cols, subplot_titles=[chart.layout.title.text for chart in charts])

    for i, chart in enumerate(charts):
        row = (i // cols) + 1
        col = (i % cols) + 1
        for trace in chart.data:
            fig.add_trace(trace, row=row, col=col)

    fig.update_layout(title=title, showlegend=False)
    return fig

def save_dashboard(fig, file_path="dashboard.html"):
    """
    Save a dashboard to an HTML file.

    Args:
        fig (plotly.graph_objects.Figure): The dashboard figure.
        file_path (str): The path to save the HTML file.

    Returns:
        None
    """
    fig.write_html(file_path)
    print(f"Dashboard saved to {file_path}")
