from preswald import text, slider, button, view, connect

# Add a header
text("# Interactive Demo")

# Add a slider
num_rows = slider("Rows to Display", min_val=1,
                  max_val=100, step=5, default=10)

# Add a button
if button("Refresh Data"):
    text("Button clicked! Refreshing data...")

# Connect to a sample CSV file
data_conn = connect("example.csv", "interactive_data")

# Display data based on slider value
text(f"### Displaying {num_rows} rows from the dataset:")
view(data_conn, limit=num_rows)
