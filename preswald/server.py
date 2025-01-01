from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
import asyncio
import os
import pkg_resources
import logging
import uvicorn
from typing import Dict, Any, Optional, Set
from preswald.scriptrunner import ScriptRunner
from preswald.core import (
    get_all_component_states,
    update_component_state,
    get_rendered_components,
    clear_rendered_components,
    connections
)
from preswald.serializer import dumps as json_dumps, loads as json_loads

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

# Store active websocket connections and their states
websocket_connections: Dict[str, WebSocket] = {}
client_states: Dict[str, Dict[str, Any]] = {}
script_runners: Dict[WebSocket, ScriptRunner] = {}

# Store persistent component states
component_states: Dict[str, Any] = {}

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

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """Handle WebSocket connections"""
    try:
        logger.info(f"[WebSocket] New connection request from client: {client_id}")
        await websocket.accept()
        logger.info(f"[WebSocket] Connection accepted for client: {client_id}")
        
        # Store the connection
        websocket_connections[client_id] = websocket
        
        # Create a script runner for this client
        script_runner = ScriptRunner(
            session_id=client_id,
            send_message_callback=_send_message_callback
        )
        script_runners[websocket] = script_runner
        
        try:
            # Send initial states
            initial_states = get_all_component_states()
            await websocket.send_json({
                "type": "initial_state",
                "states": initial_states
            })
            
            # Run the script initially
            if SCRIPT_PATH:
                await script_runner.start(SCRIPT_PATH)
            
            # Handle incoming messages
            while True:
                try:
                    message = await websocket.receive_text()
                    await handle_websocket_message(websocket, message)
                except json.JSONDecodeError as e:
                    logger.error(f"[WebSocket] JSON decode error: {e}")
                    await send_error(websocket, "Invalid message format")
                except Exception as e:
                    logger.error(f"[WebSocket] Error handling message: {e}")
                    await send_error(websocket, "Error processing message")
                    
        except WebSocketDisconnect:
            logger.info(f"[WebSocket] Client disconnected: {client_id}")
        except Exception as e:
            logger.error(f"[WebSocket] Error in connection handler: {e}")
            await send_error(websocket, f"Connection error: {str(e)}")
    finally:
        # Clean up
        websocket_connections.pop(client_id, None)
        if websocket in script_runners:
            runner = script_runners.pop(websocket)
            await runner.stop()

async def handle_websocket_message(websocket: WebSocket, message: str):
    """Handle incoming WebSocket messages"""
    try:
        data = json_loads(message)
        logger.debug(f"[WebSocket] Received message: {data}")
        
        msg_type = data.get('type')
        if not msg_type:
            logger.error("[WebSocket] Message missing type field")
            await send_error(websocket, "Message missing type field")
            return

        if msg_type == 'component_update':
            states = data.get('states', {})
            if not states:
                logger.warning("[WebSocket] Component update missing states")
                await send_error(websocket, "Component update missing states")
                return
                
            logger.info("[Component Update] Processing updates:")
            for component_id, value in states.items():
                try:
                    # Update component state
                    update_component_state(component_id, value)
                    logger.info(f"  - Updated {component_id}: {value}")
                    
                    # Broadcast to other clients
                    await broadcast_state_update(component_id, value, exclude_client=websocket)
                    logger.info(f"  - Broadcasted {component_id} update")
                except Exception as e:
                    logger.error(f"Error updating component {component_id}: {e}")
                    await send_error(websocket, f"Failed to update component {component_id}")
                    continue

            # Trigger script rerun with all states
            logger.info(f"[Script Rerun] Triggering with states: {states}")
            await rerun_script(websocket, states)

    except json.JSONDecodeError as e:
        logger.error(f"[WebSocket] Error decoding message: {e}")
        await send_error(websocket, "Invalid message format")
    except Exception as e:
        logger.error(f"[WebSocket] Error processing message: {e}")
        await send_error(websocket, f"Error processing message: {str(e)}")

async def send_error(websocket: WebSocket, message: str):
    """Send error message to client"""
    try:
        error_msg = {
            "type": "error",
            "content": {
                "message": message
            }
        }
        await websocket.send_json(error_msg)
    except Exception as e:
        logger.error(f"Error sending error message: {e}")

async def broadcast_state_update(component_id: str, value: Any, exclude_client: WebSocket = None):
    """Broadcast state update to all clients except the sender"""
    update_msg = {
        "type": "state_update",
        "component_id": component_id,
        "value": value
    }
    
    try:
        for client in websocket_connections.values():
            if client != exclude_client:
                await client.send_json(update_msg)
    except Exception as e:
        logger.error(f"Error broadcasting state update: {e}")

async def rerun_script(websocket: WebSocket, states: Dict[str, Any]):
    """Rerun the script with updated states"""
    try:
        runner = script_runners.get(websocket)
        if runner:
            await runner.rerun(states)
        else:
            logger.error("[Script Rerun] No script runner found for websocket")
            await send_error(websocket, "Script runner not found")
    except Exception as e:
        logger.error(f"[Script Rerun] Error: {e}")
        await send_error(websocket, f"Script rerun failed: {str(e)}")

async def broadcast_message(msg: dict):
    """Broadcast a message to all connected clients"""
    try:
        for websocket in websocket_connections.values():
            await websocket.send_json(msg)
    except Exception as e:
        logger.error(f"Error broadcasting message: {e}")

def _send_message_callback(msg: dict):
    """Callback for sending messages from ScriptRunner"""
    async def _send():
        try:
            for websocket in websocket_connections.values():
                await websocket.send_json(msg)
        except Exception as e:
            logger.error(f"Error in send message callback: {e}")
    
    # Create and run the task in the event loop
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(_send())
    else:
        loop.run_until_complete(_send())
    return None  # Return None to avoid awaiting this callback

@app.get("/api/connections")
async def get_connections():
    """Get all active connections"""
    try:
        connection_list = []
        for name, conn in connections.items():
            conn_type = type(conn).__name__
            conn_info = {
                "name": name,
                "type": conn_type,
                "details": str(conn)[:100] + "..." if len(str(conn)) > 100 else str(conn)
            }
            connection_list.append(conn_info)
        return {"connections": connection_list}
    except Exception as e:
        logger.error(f"Error getting connections: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def start_server(script=None, port=8501):
    """
    Start the FastAPI server.

    Args:
        script (str, optional): Path to the script to run. Defaults to None.
        port (int, optional): The port to run the server on. Defaults to 8501.
    """
    print(f"Starting Preswald server at http://localhost:{port}")
    global SCRIPT_PATH

    if script:
        SCRIPT_PATH = os.path.abspath(script)
        print(f"Will run script: {SCRIPT_PATH}")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
