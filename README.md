# Preswald SDK

[![PyPI version](https://badge.fury.io/py/preswald-sdk.svg)](https://pypi.org/project/preswald-sdk/)
[![Build Status](https://github.com/your-org/preswald-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/preswald-sdk/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Preswald SDK is an open-source, lightweight framework designed for building and managing data workflows, tailored for small teams, startups, and individual practitioners. It simplifies data ingestion, transformation, visualization, and deployment in a single, cohesive platform.

---

## ✨ Key Features

### 🔄 Data Ingestion
- **Connectors**: Pull data from files (CSV, JSON), APIs, databases (PostgreSQL, SQLite), or tools like Google Sheets.
- **Scheduling**: Set up periodic ingestion tasks with built-in scheduling.
- **Pluggable Architecture**: Add custom connectors for additional data sources.

### ⚙️ Data Transformation
- **SQL and Python Transformations**: Write SQL scripts or Python-based transformations directly.
- **Prebuilt Templates**: Templates for deduplication, aggregation, and data cleaning.
- **Data Modeling**: Reusable data models to define relationships between raw and transformed data.

### 📊 Data Visualization
- **Integrated Dashboards**: Create dashboards with KPIs, charts, and tables.
- **Drag-and-Drop Editor**: Non-technical users can arrange visualizations effortlessly.
- **Export Options**: Share dashboards via PDF or public links.

### 🚀 Deployment
- **One-Click Deployment**: Deploy to platforms like Vercel with minimal setup.
- **Real-Time Previews**: Share live previews of your app during development.

### 📈 Monitoring & Logging
- **Execution Logs**: View pipeline success/failure statuses and debug logs.
- **Data Lineage**: Track how data flows and transforms through your pipelines.

### 🛠️ Extensibility
- **Plugin System**: Add custom connectors, transformations, and visualizations.
- **Advanced Processing**: Write Python scripts for custom logic or integrations.

---

## 🚀 Why Choose Preswald?

1. **Streamlined Data Stack**: A simplified alternative to modern tools like dbt, Airflow, and Looker.
2. **End-to-End Solution**: Handles everything from ingestion to visualization in one package.
3. **Low Complexity**: No heavy infrastructure or DevOps expertise required.
4. **Designed for Small Teams**: Perfect for startups, freelancers, and non-technical collaborators.
5. **Open Source**: Transparent and community-driven development under Apache 2.0 license.

---

## 📦 Installation

To install the latest release, run:

```bash
pip install preswald-sdk
```

---

## 🏁 Quick Start Guide

### 1. Initialize a New Project
```bash
preswald init my_project
cd my_project
```

### 2. Start a Local Server
```bash
preswald run
```

### 3. Define and Run a Pipeline
```python
from preswald_sdk.ingestion import ingest
from preswald_sdk.transform import transform
from preswald_sdk.visualize import visualize
from preswald_sdk.pipeline import pipeline

# Define a pipeline
pipeline = pipeline.create(
    name="example_pipeline",
    steps=[
        ingest.from_csv("data/sales.csv"),
        transform.clean_nulls,
        visualize.create_dashboard(title="Sales Dashboard")
    ]
)

# Run the pipeline
pipeline.run()
```

### 4. Deploy to Vercel
```bash
preswald deploy
```

---

## 🛠️ CLI Commands

The **Preswald CLI** simplifies development and deployment tasks. Below are some commonly used commands:

| Command                     | Description                                                     |
|-----------------------------|-----------------------------------------------------------------|
| `preswald init [project]`   | Initialize a new project with a prebuilt folder structure.      |
| `preswald run`              | Start a local server to preview your app in real-time.         |
| `preswald pipeline run`     | Execute a specific pipeline with detailed logging.             |
| `preswald deploy`           | Deploy your app to Vercel with one click.                      |
| `preswald debug`            | Debug your pipelines interactively.                            |

For a full list of commands, run:
```bash
preswald --help
```

---

## 🔧 Configuration

### `preswald.config.json`
The configuration file defines pipelines, data sources, and environment variables for your app. Example:

```json
{
  "pipelines": [
    {
      "name": "load_data",
      "steps": [
        "ingestion/csv_ingestion.py",
        "transformations/clean_data.sql",
        "transformations/aggregate_sales.sql"
      ]
    }
  ],
  "database": {
    "type": "postgres",
    "connection_string": "postgres://user:password@localhost:5432/dbname"
  }
}
```

### `.env`
Use the `.env` file to store sensitive information like API keys:
```
DATABASE_URL=postgres://user:password@localhost:5432/dbname
API_KEY=your-api-key
```

---

## 📂 Project Structure

When you initialize a project using `preswald init`, the following structure is created:

```plaintext
my_project/
├── ingestion/              # Data ingestion scripts
│   ├── csv_ingestion.py    # Example: Load data from CSV
│
├── transformations/        # SQL/Python transformation scripts
│   ├── clean_data.sql      # Example: Remove nulls
│   ├── aggregate_sales.sql # Example: Aggregate sales data
│
├── dashboards/             # Dashboard configurations
│   ├── dashboard.json      # Example: Define a sales dashboard
│
├── models/                 # Reusable SQL models
│   ├── sales_summary.sql   # Example: Sales summary model
│
├── .env                    # Environment variables
├── preswald.config.json    # App configuration
├── requirements.txt        # Python dependencies
├── README.md               # Documentation
└── Dockerfile              # Optional: For containerized deployment
```

---

## 🧪 Testing

Preswald SDK includes a comprehensive testing suite. To run tests:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   pytest
   ```

---

## 🤝 Contributing

We welcome contributions! Here's how you can get involved:
1. Fork this repository and clone your fork.
2. Create a new feature branch:
   ```bash
   git checkout -b my-feature
   ```
3. Make your changes and write tests.
4. Run tests to ensure everything works:
   ```bash
   pytest
   ```
5. Submit a pull request!

---

## 📄 License

Preswald SDK is licensed under the [Apache 2.0 License](LICENSE). You are free to use, modify, and distribute this software, provided you comply with the license terms.

---

## 📞 Support

If you encounter any issues or have feature requests, please open an issue on our [GitHub repository](https://github.com/your-org/preswald/issues).

---

## 🔗 Resources

- [Documentation](https://your-docs-link.com)
- [PyPI Package](https://pypi.org/project/preswald/)
- [Contributor Guide](https://github.com/your-org/preswald-sdk/CONTRIBUTING.md)
