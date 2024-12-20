# **Preswald SDK**

_Your lightweight companion for building simple, interactive, and dynamic data apps in Python._

[![Apache 2.0 License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/your-repo/ci.yml?branch=main)](https://github.com/your-org/preswald/actions)
[![Coverage](https://img.shields.io/codecov/c/github/your-org/preswald)](https://codecov.io/gh/your-org/preswald)

---

### **What is Preswald?**

Preswald is your no-fuss, Python-based framework for building interactive data apps—no HTML, JavaScript, or CSS required. Whether you're a data analyst, scientist, or curious tinkerer, Preswald lets you connect to data, build interactive components, and deploy your ideas faster than you can say “dashboard.”

---

### **✨ Features**

- **Simple Markdown Rendering**: Use `preswald.text()` to convert Markdown into sleek, responsive content.
- **Data Connections Made Easy**: Connect to CSV, JSON, Parquet, or SQL databases in seconds.
- **Interactive Components**: Build with sliders, buttons, dropdowns, and more—because who doesn’t love sliders?
- **Dynamic Tables**: Preview and manipulate your data interactively.
- **Fully Customizable Themes**: Your app, your brand—just tweak `config.toml`.
- **Local Deployment**: Go live on your machine with a single command.

---

### **🚀 Getting Started**

#### **Installation**

First, install Preswald using pip. It’s quick, painless, and you’ll love it:

```bash
pip install preswald
```

---

### **👩‍💻 Quick Start**

#### **1. Initialize a New Project**

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

---

#### **2. Write Your First App**

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

---

#### **3. Run Your App**

Now the fun part—see it in action! Run your app locally with:

```bash
preswald run hello.py
```

This command launches a development server, and Preswald will let you know where your app is hosted. Typically, it’s here:

```
🌐 App running at: http://localhost:8501
```

Open your browser, and voilà—your first Preswald app is live!

---

### **🌍 Local Deployment**

When you’re ready to share your app with colleagues or test it outside your development environment, deploy it locally. This process is as simple as pie.

#### **Steps for Local Deployment:**

1. **Prepare Your Environment**  
   Make sure all your dependencies are installed:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run Your App on a Custom Port**  
   Want to run your app on a different port? No problem! Just specify the port:

   ```bash
   preswald run hello.py --port 8080
   ```

3. **Share Your Local App**  
   If you’re on the same network, others can access your app by visiting your machine’s IP address. Use `ifconfig` (Linux/Mac) or `ipconfig` (Windows) to find your local IP, and share the URL:

   ```
   http://<your-ip>:8080
   ```

4. **Keep Your App Alive**  
   Use tools like `tmux` or `screen` to keep the app running even when you close the terminal.

---

### **💡 Examples**

#### **Example 1: Hello World**

```python
from preswald import text

text("# Hello, World!")
```

#### **Example 2: Data Viewer**

```python
from preswald import connect, view

data_conn = connect("example.csv", "example_data")
view(data_conn)
```

#### **Example 3: Interactive Dashboard**

```python
from preswald import text, slider, view, connect

text("# Interactive Dashboard")

slider_value = slider("Rows to Display", min_val=10, max_val=100, step=10, default=50)
data_conn = connect("example.csv", "data")
view(data_conn, limit=slider_value)
```

---

### **🔧 Configuration**

Preswald uses `config.toml` for project settings and theming. It’s straightforward, and it makes your app look polished.

#### **Sample `config.toml`:**

```toml
[theme.color]
primary = "#3498db"
secondary = "#e74c3c"
background = "#f5f5f5"
text = "#333333"

[theme.font]
family = "Roboto, sans-serif"
size = "14px"

[theme.layout]
sidebar_width = "280px"
```

---

### **📚 Documentation**

We’re here to help! Check out our full documentation at [Preswald Docs](https://github.com/your-org/preswald/wiki).

---

### **🤝 Contributing**

Preswald thrives on community contributions! Here’s how you can help:

1. Fork the repository.
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/preswald.git
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run tests:
   ```bash
   pytest
   ```

Submit a pull request, and we’ll review it faster than you can say “interactive dashboard!”

For details, check out [CONTRIBUTING.md](CONTRIBUTING.md).

---

### **📄 License**

Preswald is licensed under the [Apache 2.0 License](LICENSE).

---

### **🎉 Join the Community**

- **GitHub Issues**: Found a bug? Let us know [here](https://github.com/your-org/preswald/issues).
- **Discussions**: Share your ideas and ask questions in our [discussion forum](https://github.com/your-org/preswald/discussions).
- **Contributors**: Meet the awesome people who make Preswald better [here](https://github.com/your-org/preswald/graphs/contributors).