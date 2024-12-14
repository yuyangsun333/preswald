import pandas as pd
from preswald.visualization import create_bar_chart, create_line_chart, create_pie_chart, create_dashboard

def test_create_bar_chart():
    data = pd.DataFrame({"x": ["A", "B", "C"], "y": [10, 20, 30]})
    chart = create_bar_chart(data, x="x", y="y", title="Test Bar Chart")
    assert chart.layout.title.text == "Test Bar Chart"

def test_create_line_chart():
    data = pd.DataFrame({"x": ["Jan", "Feb", "Mar"], "y": [100, 200, 300]})
    chart = create_line_chart(data, x="x", y="y", title="Test Line Chart")
    assert chart.layout.title.text == "Test Line Chart"

def test_create_pie_chart():
    data = pd.DataFrame({"names": ["A", "B", "C"], "values": [30, 20, 50]})
    chart = create_pie_chart(data, names="names", values="values", title="Test Pie Chart")
    assert chart.layout.title.text == "Test Pie Chart"

def test_create_dashboard():
    data = pd.DataFrame({"x": ["A", "B", "C"], "y": [10, 20, 30]})
    bar_chart = create_bar_chart(data, x="x", y="y", title="Test Bar Chart")
    dashboard = create_dashboard([bar_chart], layout=(1, 1), title="Test Dashboard")
    assert dashboard.layout.title.text == "Test Dashboard"
