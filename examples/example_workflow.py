from preswald.ingestion import from_csv, from_api, from_postgres, from_google_sheets

# Load data from a CSV file
csv_data = from_csv("data/sales.csv")

# Fetch data from a REST API
api_data = from_api(
    url="https://api.example.com/data",
    headers={"Authorization": "Bearer token"}
)

# Query data from a PostgreSQL database
postgres_data = from_postgres(
    connection_string="postgresql://user:password@localhost:5432/dbname",
    query="SELECT * FROM sales"
)

# Load data from Google Sheets
sheets_data = from_google_sheets(
    sheet_id="1abcdEFGHIjklMNO12345PQRSTUV",
    range_name="Sheet1!A1:D10",
    creds_path="path/to/credentials.json"
)
