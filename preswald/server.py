from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
import uvicorn
import os

# Initialize FastAPI application
app = FastAPI()

# Configure Jinja2 environment for templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# Mount static assets (e.g., CSS, JS)
STATIC_DIR = os.path.join(BASE_DIR, "assets")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
async def render_app():
    """
    Render the main Preswald app.

    Returns:
        HTMLResponse: Rendered HTML content.
    """
    try:
        # Dynamically import the user script
        from user_script import render  # User-defined `render` function
        content = render()
    except ImportError as e:
        # Fallback if user script is missing or incorrect
        content = f"<h1>Error loading user script</h1><p>{e}</p>"

    # Load base HTML template and inject content
    template = env.get_template("base.html")
    rendered_html = template.render(content=content)
    return HTMLResponse(content=rendered_html)


@app.post("/interact")
async def handle_interaction(request: Request):
    """
    Handle user interactions (e.g., button clicks, slider changes).

    Args:
        request (Request): Incoming POST request.
    Returns:
        dict: Response with updated data or UI.
    """
    payload = await request.json()
    event_type = payload.get("type")
    event_data = payload.get("data")

    # Handle different event types dynamically
    if event_type == "button_click":
        return {"message": f"Button '{event_data}' clicked!"}
    elif event_type == "slider_change":
        return {"value": event_data}
    else:
        return {"message": "Unknown interaction type"}


def start_server(script="hello.py", port=8501):
    """
    Start the Preswald server and load the user script.

    Args:
        script (str): Path to the user script to load.
        port (int): Port to run the server on.
    """
    # Dynamically load the user script
    try:
        with open("user_script.py", "w") as f:
            with open(script, "r") as user_script:
                f.write(user_script.read())
    except FileNotFoundError:
        print(f"Error: File '{script}' not found.")
        return

    print(f"Starting Preswald server at http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
