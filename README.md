![Banner](assets/banner.png)

<h1 align="center">Preswald SDK</h1>

<p align="center">
    <em>Your lightweight companion for building simple, interactive, and dynamic data apps in Python.</em>
</p>
<p align="center">
    <a href="LICENSE">
        <img src="https://img.shields.io/badge/license-Apache%202.0-blue.svg" alt="Apache 2.0 License">
    </a>
    <a href="https://www.python.org/downloads/">
        <img src="https://img.shields.io/badge/python-3.7%2B-blue.svg" alt="Python Version">
    </a>
<p align="center">
    <a href="https://structured-users.slack.com/join/shared_invite/zt-265ong01f-UHP6BP3FzvOmMQDIKty_JQ#/shared-invite/email">
        <img src="https://img.shields.io/badge/Slack-Join%20Community-orange" alt="Slack Community">
    </a>
</p>
</p>


## **What is Preswald?**

Preswald is a full-stack platform for building, deploying, and managing interactive data applications. It combines ingestion, storage, transformation, and visualization into one lightweight and powerful SDK. Whether you're prototyping internal tools or deploying production-grade apps, Preswald reduces complexity and cost without compromising flexibility.

- Code-First Simplicity. Minimal Python and SQL for powerful apps
- End-to-End Coverage. Handle ingestion, ETL, and visualization in one platform
- Efficient by Design. Avoid the sprawling complexity of the modern data stack while keeping what works.
- Connect to CSV, JSON, Parquet, or SQL databases in seconds.
- Fully Customizable Themes. Your app, your brand—just tweak images and names in `config.toml`.
- Go live on your machine with a single command.

<br>

---

# **🚀 Getting Started**

## **Installation**

First, install Preswald using pip. https://pypi.org/project/preswald/ 

```bash
pip install preswald
```

![Demo GIF](assets/demo1.gif)

## **👩‍💻 Quick Start**

### **1. Initialize a New Project**

Start your journey with Preswald by initializing a new project:

```bash
preswald init my_project
cd my_project
```

This will create a folder called `my_project` with all the basics you need:

- `hello.py`: Your first Preswald app.
- `config.toml`: Customize your app’s settings and style.
- `secrets.toml`: Keep your API keys and sensitive information safe.
- `.gitignore`: Preconfigured to keep `secrets.toml` out of your Git repository.


### **2. Write Your First App**

Time to make something magical! Open up `hello.py` and write:

```python
from preswald import text, connect, view

# Render Markdown content
text("# Welcome to Preswald")

# Connect to a CSV file
data_conn = connect("example.csv", "my_data")

# Display the data as a table
view(data_conn)
```
![Demo GIF](assets/demo2.gif)


### **3. Run Your App**

Now the fun part—see it in action! Run your app locally with:

```bash
preswald run hello.py
```

This command launches a development server, and Preswald will let you know where your app is hosted. Typically, it’s here:

```
🌐 App running at: http://localhost:8501
```

Open your browser, and voilà—your first Preswald app is live!



## **💡 Examples**

### **Example 1: Hello World**

```python
from preswald import text

text("# Hello, World!")
```

### **Example 2: Data Viewer**

```python
from preswald import connect, view

data_conn = connect("example.csv", "example_data")
view(data_conn)
```

### **Example 3: Interactive Dashboard**

```python
from preswald import text, slider, view, connect

text("# Interactive Dashboard")

slider_value = slider("Rows to Display", min_val=10, max_val=100, step=10, default=50)
data_conn = connect("example.csv", "data")
view(data_conn, limit=slider_value)
```

## **🔧 Configuration**

Preswald uses `config.toml` for project settings and theming. It’s straightforward, and it makes your app look polished.

### **Sample `config.toml`:**

```
[project]
title = "Preswald Project"
version = "0.1.0"
port = 8501

[branding]
logo = "thumbnail.png"
favicon = "favicon.ico"
name = "My app"

[theme.color]
primary = "#4CAF50"
secondary = "#FFC107"
background = "#FFFFFF"
text = "#000000"

[theme.font]
family = "Arial, sans-serif"
size = "16px"

[connections.postgres_main]
type = "postgres"
host = "localhost"
port = 5432
dbname = "mydb"
user = "user"

# password is stored in secrets.toml

[connections.earthquake_data]
type = "csv"
path = "earthquake_data.csv"
```

---

## **📚 Documentation**

We’re here to help! Check out our full documentation at [Preswald Docs](https://docs.preswald.com/).

---

## **🤝 Contributing**

Preswald thrives on community contributions! Here’s how you can help:

1. Fork the repository.
2. Clone your fork:
   ```bash
   git clone https://github.com/StructuredLabs/preswald.git
   ```
3. For local development, with the frontend, run the following commands

   ```
   pip install -e ".[dev]"
   python setup.py build_frontend
   python -m build
   pip install dist/preswald-0.xx.xx.tar.gz
   ```

4. Run a test app
   ```
   preswald run examples/earthquakes.py
   ```


For details, check out [CONTRIBUTING.md](CONTRIBUTING.md).

---

## **🎉 Join the Community**

- **GitHub Issues**: Found a bug? Let us know [here](https://github.com/StructuredLabs/preswald/issues).
- **Community Forum**: Reach out [here](https://structured-users.slack.com/join/shared_invite/zt-265ong01f-UHP6BP3FzvOmMQDIKty_JQ#/shared-invite/email)
- **Discussions**: Share your ideas and ask questions in our [discussion forum](https://github.com/StructuredLabs/preswald/discussions).
- **Contributors**: Meet the awesome people who make Preswald better [here](https://github.com/StructuredLabs/preswald/graphs/contributors).

---

### **📄 License**

Preswald is licensed under the [Apache 2.0 License](LICENSE).

