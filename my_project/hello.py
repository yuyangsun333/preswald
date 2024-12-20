from preswald import text, slider, checkbox, selectbox, connect, view

# Add a header
text("# Welcome to My Preswald App")

# Add a slider for interactivity
value = slider("Select a value", min_val=1, max_val=100, default=50)
text(f"### You selected: {value}")

# Add a checkbox
accepted = checkbox("Do you accept the terms?", default=False)
if accepted:
    text("### Thank you for accepting the terms!")

# Add a dropdown for selection
choice = selectbox("Choose a category", options=[
                   "Option 1", "Option 2", "Option 3"], default="Option 1")
text(f"### You selected: {choice}")

# Connect to a CSV file and display data
data_conn = connect("example.csv", "data_connection")
text("### Data Preview:")
view(data_conn)
