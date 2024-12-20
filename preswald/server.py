from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
import uvicorn
import os

# Initialize FastAPI app
app = FastAPI()

# Configure Jinja2 for template rendering
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


@app.get("/", response_class=HTMLResponse)
async def render_home():
    """
    Render the homepage using base.html and inject custom content.
    """
    try:
        # Load base.html and pass variables to the template
        template = env.get_template("base.html")
        html_content = template.render(
            title="Preswald App",
            theme={
                "font": {"family": "Arial, sans-serif", "size": "16px"},
                "color": {
                    "primary": "#4CAF50",
                    "secondary": "#FFC107",
                    "background": "#FFFFFF",
                    "text": "#000000",
                },
                "layout": {"sidebar_width": "250px"},
            },
        )
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(
            content=f"<h1>Error Rendering Template</h1><p>{e}</p>", status_code=500
        )


@app.get("/components", response_class=HTMLResponse)
async def render_components():
    """
    Render components.html with example interactive elements.
    """
    try:
        # Load components.html and pass variables to the template
        template = env.get_template("components.html")
        html_content = template.render(
            components=[
                {"type": "button", "label": "Click Me"},
                {"type": "slider", "label": "Adjust Volume", "min": 0, "max": 100},
            ]
        )
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(
            content=f"<h1>Error Rendering Template</h1><p>{e}</p>", status_code=500
        )


def start_server(script="hello.py", port=8501):
    """
    Start the Preswald server.

    Args:
        script (str): The Python script to load (currently a placeholder for dynamic functionality).
        port (int): The port to run the server on.
    """
    print(f"Starting Preswald server for {script} at http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
