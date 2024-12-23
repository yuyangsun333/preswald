from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from preswald.scriptrunner import ScriptRunner
from typing import Dict, Any, Optional
import os
import uvicorn
import json
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

SCRIPT_PATH: Optional[str] = None

# Store active websocket connections
websocket_connections: Dict[str, WebSocket] = {}

# Paths for production build
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "../frontend/dist"))
ASSETS_DIR = os.path.join(STATIC_DIR, "assets")

# Mount static files for production
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
app.mount("/public", StaticFiles(directory=os.path.join(BASE_DIR, "../frontend/public")), name="public")

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
        if SCRIPT_PATH:
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


@app.get("/", include_in_schema=False)
async def serve_home():
    """
    Serve React's index.html in production, or redirect to the React dev server in development.
    """
    dev_server_url = "http://localhost:3000"  # React dev server URL
    try:
        # Check if React dev server is running
        import httpx

        async with httpx.AsyncClient() as client:
            response = await client.get(dev_server_url)
        if response.status_code == 200:
            # Redirect to React dev server
            return RedirectResponse(dev_server_url)
    except:
        pass  # If dev server is not running, serve production build

    # Serve the production build if React dev server isn't running
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="React app not found")


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


@app.get("/logo.png")
async def serve_logo():
    """Serve the logo file."""
    logo_path = os.path.join(BASE_DIR, "../frontend/public/logo.png")
    if os.path.exists(logo_path):
        return FileResponse(logo_path)
    # Return a default image or 404
    raise HTTPException(status_code=404, detail="Logo not found")
