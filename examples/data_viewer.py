from preswald import text, connect, view

# Add a header
text("# Data Viewer")

# Connect to a sample CSV file
data_conn = connect("example.csv", "example_data")

# Display a preview of the data
text("### Here's a preview of your data:")
view(data_conn)
