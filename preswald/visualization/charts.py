import plotly.express as px

def create_bar_chart(data, x, y, title="Bar Chart"):
    """
    Create a bar chart.

    Args:
        data (pd.DataFrame): The input data.
        x (str): Column name for x-axis.
        y (str): Column name for y-axis.
        title (str): Title of the chart.

    Returns:
        plotly.graph_objects.Figure: The bar chart.
    """
    fig = px.bar(data, x=x, y=y, title=title)
    return fig

def create_line_chart(data, x, y, title="Line Chart"):
    """
    Create a line chart.

    Args:
        data (pd.DataFrame): The input data.
        x (str): Column name for x-axis.
        y (str): Column name for y-axis.
        title (str): Title of the chart.

    Returns:
        plotly.graph_objects.Figure: The line chart.
    """
    fig = px.line(data, x=x, y=y, title=title)
    return fig

def create_pie_chart(data, names, values, title="Pie Chart"):
    """
    Create a pie chart.

    Args:
        data (pd.DataFrame): The input data.
        names (str): Column name for pie section names.
        values (str): Column name for pie section values.
        title (str): Title of the chart.

    Returns:
        plotly.graph_objects.Figure: The pie chart.
    """
    fig = px.pie(data, names=names, values=values, title=title)
    return fig
