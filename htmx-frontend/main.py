import asyncio
import json
import logging
import uuid

import websockets
from client import app

from preswald.engine.server_service import ServerPreswaldService


# Set up logging
logging.basicConfig(level=logging.INFO)
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
                logger.info("Registering directly with local Preswald service")
                # We need to create a custom WebSocket-like object that implements
                # the necessary methods that ServerPreswaldService.register_client expects
                self.websocket = MockWebSocket()
                self.script_runner = await self.service.register_client(
                    self.client_id, self.websocket
                )
                self.connected = True
                logger.info(f"Successfully registered client with ID: {self.client_id}")
                return True
            else:
                # If we don't have direct access, connect via WebSocket
                try:
                    # Connect to the external Preswald service
                    ws_url = f"{preswald_url}/{self.client_id}"
                    logger.info(f"Connecting to Preswald service at {ws_url}")

                    # Create a background task to maintain the connection
                    self.connection_task = asyncio.create_task(
                        self._maintain_external_connection(ws_url)
                    )

                    self.connected = True
                    logger.info("Started connection task to Preswald service")
                    return True
                except Exception as e:
                    logger.error(f"Failed to connect to external Preswald service: {e}")
                    return False
        except Exception as e:
            logger.error(f"Failed to connect to Preswald: {e}")
            return False

    async def _maintain_external_connection(self, ws_url):
        """Maintain a connection to the external Preswald service"""
        while True:
            try:
                async with websockets.connect(ws_url) as websocket:
                    logger.info(f"Connected to external Preswald service at {ws_url}")
                    self.external_ws = websocket

                    # Keep the connection alive
                    while True:
                        # Receive messages from Preswald
                        message = await websocket.recv()
                        logger.info(f"Received message from Preswald: {message}")

                        # Process the message (you might want to do something with it)
                        try:
                            data = json.loads(message)
                            # Handle different message types
                            if data.get("type") == "components":
                                # Update the UI with the components
                                logger.info("Received components from Preswald")
                            elif data.get("type") == "state_update":
                                # Update the state
                                logger.info("Received state update from Preswald")
                        except Exception as e:
                            logger.error(f"Error processing message: {e}")

            except Exception as e:
                logger.error(f"WebSocket connection error: {e}")
                self.external_ws = None
                # Wait before reconnecting
                await asyncio.sleep(3)

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
async def ws(msg: str, send):
    """Handle WebSocket messages and forward them to Preswald"""
    global preswald_connection

    try:
        if not preswald_connection or not preswald_connection.connected:
            await send("Error: Not connected to Preswald service")
            return

        # Forward message to Preswald
        success = await preswald_connection.send_message(
            {"type": "message", "content": msg, "source": "htmx-frontend"}
        )

        if success:
            await send(f"Message sent to Preswald: {msg}")
        else:
            await send("Failed to send message to Preswald")
    except Exception as e:
        logger.error(f"Error handling WebSocket message: {e}")
        await send(f"Error: {e!s}")


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
