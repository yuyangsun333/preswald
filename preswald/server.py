from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from preswald.scriptrunner import ScriptRunner
from preswald.themes import load_theme
from typing import Dict, Any, Optional
import os
import uvicorn
import json
from collections import defaultdict
import logging
import pkg_resources

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCRIPT_PATH: Optional[str] = None

# Store active websocket connections
websocket_connections: Dict[str, WebSocket] = {}

try:
    # Get the package's static directory using pkg_resources
    BASE_DIR = pkg_resources.resource_filename('preswald', '')
    STATIC_DIR = os.path.join(BASE_DIR, "static")
    ASSETS_DIR = os.path.join(STATIC_DIR, "assets")

    # Ensure directories exist
    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(ASSETS_DIR, exist_ok=True)

    # Mount static files only if directories exist and contain files
    if os.path.exists(ASSETS_DIR) and os.listdir(ASSETS_DIR):
        app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
        logger.info(f"Mounted assets directory: {ASSETS_DIR}")
    else:
        logger.warning(f"Assets directory not found or empty: {ASSETS_DIR}")

except Exception as e:
    logger.error(f"Error setting up static files: {str(e)}")
    raise

@app.get("/")
async def serve_index():
    """Serve the index.html file"""
    try:
        index_path = os.path.join(STATIC_DIR, "index.html")
        if os.path.exists(index_path):
            # Load config if script path is set
            title = "Preswald"  # Default title
            if SCRIPT_PATH:
                try:
                    config_path = os.path.join(os.path.dirname(SCRIPT_PATH), "config.toml")
                    print(f"Loading config from {config_path}")
                    import toml
                    config = toml.load(config_path)
                    print(f"Loaded config in server.py: {config}")
                    print(f"Loaded config in server.py title: {config.get('project', {}).get('title')}")
                    if config.get("project", {}).get("title"):
                        title = config["project"]["title"]
                except Exception as e:
                    logger.error(f"Error loading config for index: {e}")

            # Read and modify the index.html content
            with open(index_path, 'r') as f:
                content = f.read()
                # Replace the title tag content
                content = content.replace('<title>Vite + React</title>', f'<title>{title}</title>')
            
            return HTMLResponse(content)
        else:
            logger.error(f"Index file not found at {index_path}")
            return HTMLResponse("<html><body><h1>Error: Frontend not properly installed</h1></body></html>")
    except Exception as e:
        logger.error(f"Error serving index: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/{path:path}")
async def serve_static(path: str):
    """Serve static files with proper error handling"""
    try:
        # Security check: prevent directory traversal
        requested_path = os.path.abspath(os.path.join(STATIC_DIR, path))
        if not requested_path.startswith(os.path.abspath(STATIC_DIR)):
            raise HTTPException(status_code=403, detail="Access denied")

        if os.path.exists(requested_path) and os.path.isfile(requested_path):
            return FileResponse(requested_path)
        elif path == "" or not os.path.exists(requested_path):
            # SPA routing - return index.html for non-existent paths
            return await serve_index()
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        logger.error(f"Error serving static file {path}: {str(e)}")
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/logo.png")
async def serve_logo():
    """Serve the logo file with proper error handling"""
    try:
        logo_path = os.path.join(STATIC_DIR, "logo.png")
        if os.path.exists(logo_path) and os.path.isfile(logo_path):
            return FileResponse(logo_path)
        raise HTTPException(status_code=404, detail="Logo not found")
    except Exception as e:
        logger.error(f"Error serving logo: {str(e)}")
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(status_code=500, detail="Internal server error")

async def broadcast_message(message: dict):
    """Broadcast message to all connected clients"""
    logger.debug(f"Broadcasting message to {len(websocket_connections)} clients: {message}")
    # Create a list of items to avoid dictionary modification during iteration
    connections = list(websocket_connections.items())
    
    for client_id, connection in connections:
        try:
            # Simply try to send the message, FastAPI's WebSocket handles state internally
            await connection.send_json(message)
            logger.debug(f"Message sent to client {client_id}")
        except Exception as e:
            logger.error(f"Error sending message to client {client_id}: {e}")
            # Remove dead connections after the loop
            websocket_connections.pop(client_id, None)

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """Handle WebSocket connections"""
    logger.info(f"New WebSocket connection request from client: {client_id}")
    await websocket.accept()
    logger.info(f"WebSocket connection accepted for client: {client_id}")
    
    # Store the connection
    websocket_connections[client_id] = websocket
    
    # Create ScriptRunner instance for this connection
    script_runner = ScriptRunner(
        session_id=client_id,
        send_message_callback=broadcast_message
    )
    
    try:
        # Load and send config immediately after connection
        if SCRIPT_PATH:
            config_path = os.path.join(os.path.dirname(SCRIPT_PATH), "config.toml")
            config = load_theme(config_path)
            await websocket.send_json({
                "type": "config",
                "config": config
            })
            logger.info(f"Sent config to client {client_id}")
            
            logger.info(f"Starting script execution for client {client_id} with script: {SCRIPT_PATH}")
            await script_runner.start(SCRIPT_PATH)
            
        while True:
            data = await websocket.receive_json()
            logger.debug(f"Received WebSocket message from client {client_id}: {data}")
            
            if data.get("type") == "component_update":
                logger.info(f"Component update from client {client_id}: {data}")
                await script_runner.rerun(new_widget_states=data.get("states", {}))
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for client: {client_id}")
    except Exception as e:
        logger.error(f"Error in websocket connection for client {client_id}: {e}", exc_info=True)
    finally:
        # Make sure to clean up the connection in all cases
        websocket_connections.pop(client_id, None)


def _send_message_callback(msg: dict):
    """
    Callback function that ScriptRunner will use to send messages back to the frontend.
    In a WebSocket setup, this would send directly through the socket.
    For HTTP, we'll need to store messages and let the frontend poll for them.
    """
    # For now, we'll just print the messages
    # In a real implementation, we might store these in a queue or database
    print(f"Message from ScriptRunner: {msg}")


# Initialize a single ScriptRunner instance for handling Python script execution
script_runner = ScriptRunner(
    session_id="default_session", send_message_callback=_send_message_callback
)


@app.get("/api/components")
async def get_components():
    """
    API to fetch dynamic components data.
    """
    return [
        {"type": "button", "label": "Click Me"},
        {"type": "slider", "label": "Adjust Volume", "min": 0, "max": 100},
        {"type": "text", "label": "Enter Name", "placeholder": "Your Name"},
        {"type": "checkbox", "label": "Agree to Terms"},
        {
            "type": "selectbox",
            "label": "Select Option",
            "options": ["Option 1", "Option 2", "Option 3"],
        },
        {"type": "progress", "label": "Loading...", "value": 50},
        {"type": "spinner", "label": "Loading..."},
        {"type": "alert", "message": "This is an alert!", "level": "info"},
        {
            "type": "image",
            "src": "https://cdn.pixabay.com/photo/2020/07/21/01/33/cute-5424776_1280.jpg",
            "alt": "Placeholder image",
        },
        {
            "type": "text_input",
            "label": "Type here",
            "placeholder": "Type something here",
        },
        {"type": "connection"},
        {
            "type": "table",
            "data": [
                {"Index": 1, "Value": 1},
                {"Index": 2, "Value": 2},
                {"Index": 3, "Value": 3},
            ],
        },
        {"type": "plot", "data": [1, 2, 3]},
    ]


@app.get("/api/run_script")
async def run_script():
    """
    API to run script.
    """
    await script_runner.start(script_path=SCRIPT_PATH)


def start_server(script=None, port=8501):
    """
    Start the FastAPI server.

    Args:
        port (int): The port to run the server on.
    """
    print(f"Starting Preswald server at http://localhost:{port}")
    global SCRIPT_PATH

    # Store the script path at module level so websocket handler can access it
    if script:
        # Convert to absolute path to avoid any relative path issues
        SCRIPT_PATH = os.path.abspath(script)
        print(f"Will run script: {SCRIPT_PATH}")
    uvicorn.run(app, host="0.0.0.0", port=port)
