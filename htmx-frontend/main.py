import asyncio
import json
import logging
import uuid

import websockets

# Import from client module
from client import app, render_components

from preswald.engine.server_service import ServerPreswaldService


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Generate a unique client ID - use a short ID similar to what Preswald uses
client_id = str(uuid.uuid4())[:6]

# Store the Preswald connection
preswald_connection = None


class PreswaldConnection:
    """Manages the connection to the Preswald service"""

    def __init__(self, client_id):
        self.client_id = client_id
        self.service = None
        self.websocket = None
        self.script_runner = None
        self.connected = False
        self.external_ws = None
        self.connection_task = None
        self.latest_components = None
        self.latest_state = None
        # Store message history
        self.message_history = []

    async def connect(self, preswald_url="ws://localhost:8501/ws"):
        """Connect to the Preswald service"""
        try:
            # First try to get the local service instance
            try:
                self.service = ServerPreswaldService.get_instance()
                logger.info("Found local Preswald service instance")
            except Exception as e:
                logger.info(f"No local service instance available: {e}")
                self.service = None

            # If we have direct access to the service, we can register directly
            if self.service:
                # Register with the service
                self.service.register_client(self.client_id)
                self.connected = True
                logger.info("Connected to local Preswald service")
                return True

            # Otherwise, connect to the external service via WebSocket
            # Generate a unique client ID if not provided
            if not self.client_id:
                self.client_id = str(uuid.uuid4())[:6]

            # Create a WebSocket connection to the Preswald service
            ws_url = f"{preswald_url}/{self.client_id}"
            logger.info(f"Connecting to Preswald service at {ws_url}")

            # Start a background task to maintain the connection
            if self.connection_task:
                # Cancel the existing task if it's running
                self.connection_task.cancel()
                try:
                    await self.connection_task
                except asyncio.CancelledError:
                    pass

            # Start a new connection task
            self.connection_task = asyncio.create_task(
                self._maintain_external_connection(ws_url)
            )
            logger.info("Started connection task to Preswald service")

            # Wait a short time to see if the connection is established
            for _ in range(10):  # Wait up to 1 second
                if self.connected:
                    return True
                await asyncio.sleep(0.1)

            # If we get here, the connection wasn't established quickly
            # But the task is still running, so we'll return True anyway
            # The connection might be established later
            return True
        except Exception as e:
            logger.error(f"Error connecting to Preswald service: {e}")
            self.connected = False
            return False

    async def _maintain_external_connection(self, ws_url):
        """Maintain a connection to the external Preswald service"""
        while True:
            try:
                # Connect to the Preswald service
                logger.info(f"Connecting to external Preswald service at {ws_url}")
                async with websockets.connect(ws_url) as websocket:
                    self.external_ws = websocket
                    self.connected = True
                    logger.info(f"Connected to external Preswald service at {ws_url}")

                    # Store the latest components and state for new clients
                    self.latest_components = None
                    self.latest_state = None

                    # Keep the connection alive
                    while True:
                        # Receive messages from Preswald
                        message = await websocket.recv()
                        logger.info(
                            f"Received message from Preswald (length: {len(message)})"
                        )

                        # Add to message history
                        self.message_history.append(message)
                        if len(self.message_history) > 100:  # Limit history size
                            self.message_history = self.message_history[-100:]

                        # Store the message for new clients
                        try:
                            data = json.loads(message)
                            if data.get("type") == "components":
                                logger.info("Received components update")
                                self.latest_components = data
                                # Here we could broadcast to all connected clients if we were tracking them
                            elif data.get("type") == "initial_state":
                                logger.info("Received initial state")
                                self.latest_state = data
                        except Exception as e:
                            logger.error(f"Error processing message: {e}")

            except Exception as e:
                logger.error(f"WebSocket connection error: {e}")
                self.external_ws = None
                self.connected = False
                # Wait before reconnecting
                await asyncio.sleep(3)

    async def broadcast_to_clients(self, message):
        """Broadcast a message to all connected clients"""
        # This is a placeholder - in a real implementation, you would track all connected clients
        # For now, we'll rely on the WebSocket handler to fetch the latest data when a client connects
        pass

    async def send_message(self, message):
        """Send a message to the Preswald service"""
        if not self.connected:
            logger.error("Not connected to Preswald service")
            return False

        try:
            if self.service:
                # Direct service access
                await self.service.handle_client_message(self.client_id, message)
                return True
            elif self.external_ws:
                # External WebSocket connection
                await self.external_ws.send(json.dumps(message))
                logger.info(f"Sent message to Preswald: {message}")
                return True
            else:
                logger.error("No connection method available")
                return False
        except Exception as e:
            logger.error(f"Error sending message to Preswald: {e}")
            return False


class MockWebSocket:
    """A mock WebSocket class that implements the necessary methods"""

    async def accept(self):
        logger.info("MockWebSocket: Connection accepted")
        return True

    async def send_json(self, data):
        logger.info(f"MockWebSocket: Sending JSON: {data}")
        # Process the message from Preswald
        if data.get("type") == "components":
            logger.info("Received components from Preswald")
        return True

    async def receive_json(self):
        # This would block in a real implementation
        # For now, just return an empty message
        await asyncio.sleep(10)  # Wait a bit to avoid tight loops
        return {"type": "ping"}

    async def close(self, code=1000, reason="Normal closure"):
        logger.info(f"MockWebSocket: Connection closed with code {code}: {reason}")
        return True


# Override the WebSocket handler to communicate with Preswald
@app.ws("/ws")
async def ws(msg: str, send):  # noqa: C901
    """Handle WebSocket messages and forward them to Preswald"""
    global preswald_connection

    try:
        # Log the message type to debug
        logger.info(
            f"WebSocket message received, type: {type(msg)}, content: {msg[:100] if isinstance(msg, str) else 'non-string'}"
        )

        # Handle ping messages
        if msg == "ping":
            logger.info("Received ping, sending pong")
            await send("pong")
            return

        # Handle debug ping messages
        if msg == "debug-ping":
            logger.info("Received debug ping, sending debug response")
            await send("Debug connection successful!")
            return

        if not preswald_connection:
            logger.error("Preswald connection not initialized")
            error_msg = "<p class='text-red-500 font-bold'>Error: Preswald connection not initialized</p>"
            logger.info(f"Sending error message: {error_msg}")
            await send(error_msg)
            return

        if not preswald_connection.connected:
            logger.error("Not connected to Preswald service")
            # Try to reconnect
            logger.info("Attempting to reconnect to Preswald service")
            connected = await preswald_connection.connect()
            if not connected:
                error_msg = """
                <div class='bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4'>
                    <p class='font-bold'>Error: Not connected to Preswald service</p>
                    <p>The server is unable to connect to the Preswald service. Please ensure the Preswald service is running.</p>
                </div>
                """
                logger.info(f"Sending error message: {error_msg}")
                await send(error_msg)
                return

        # Handle initial connection or empty message - send the latest components
        is_empty_message = msg is None or (isinstance(msg, str) and msg.strip() == "")

        if is_empty_message or msg == "{}":  # Empty message or refresh request
            logger.info("Initial connection or refresh request, sending components")

            # Get the latest components message
            latest_components = None
            message_count = 0
            for message in reversed(preswald_connection.message_history):
                message_count += 1
                try:
                    data = json.loads(message)
                    logger.info(
                        f"Checking message {message_count}: type={data.get('type')}"
                    )
                    if data.get("type") == "components":
                        latest_components = data
                        logger.info(
                            f"Found latest components: {len(data.get('components', {}).get('rows', []))} rows"
                        )
                        break
                except Exception as e:
                    logger.error(f"Error parsing message: {e}")
                    continue

            if latest_components:
                # Convert components to HTML
                html_content = render_components(latest_components)
                logger.info(f"Sending HTML content (length: {len(html_content)})")
                await send(html_content)
            else:
                logger.warning("No components found in message history")
                await send(
                    "<p class='text-yellow-500 font-bold'>No components data available yet. Please wait...</p>"
                )
        else:
            logger.info("Received unknown message type, sending components")

            # For now, just send the latest components for any message
            if preswald_connection.latest_components:
                html_content = render_components(preswald_connection.latest_components)
                logger.info(f"Sending HTML content (length: {len(html_content)})")
                await send(html_content)
            else:
                logger.warning("No components available")
                await send(
                    "<p class='text-yellow-500 font-bold'>No components data available yet. Please wait...</p>"
                )

    except Exception as e:
        logger.error(f"Error handling WebSocket message: {e}")
        error_html = f"""
        <div class='bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4'>
            <p class='font-bold'>Server Error</p>
            <p>{e!s}</p>
            <p class='text-xs mt-2'>Please check the server logs for more details.</p>
        </div>
        """
        await send(error_html)


async def startup():
    """Initialize the Preswald connection on startup"""
    global preswald_connection
    preswald_connection = PreswaldConnection(client_id)
    connected = await preswald_connection.connect()
    if connected:
        logger.info("Successfully connected to Preswald service")
    else:
        logger.error("Failed to connect to Preswald service")


# Add startup event handler to FastAPI app
app.add_event_handler("startup", startup)

if __name__ == "__main__":
    # Start the FastHTML app
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
