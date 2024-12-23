import sys
import traceback
import logging
from contextlib import contextmanager
from typing import Dict, Callable, Optional
import asyncio

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ScriptRunner:
    def __init__(self, session_id: str, send_message_callback: Callable):
        self.session_id = session_id
        self.send_message = send_message_callback
        self.script_path: Optional[str] = None
        self.widget_states: Dict = {}
        self._is_running = False
        self.session_state = {}
        logger.info(f"ScriptRunner initialized with session_id: {session_id}")

    async def start(self, script_path: str = "app.py"):
        """Start running the script"""
        logger.info(f"Starting script execution: {script_path}")
        self.script_path = script_path
        self._is_running = True
        await self.run_script()

    async def stop(self):
        """Stop the script runner"""
        logger.info("Stopping script runner")
        self._is_running = False

    async def rerun(self, new_widget_states: Dict = None):
        """Rerun the script with potentially new widget values"""
        logger.info(f"Rerunning script with new states: {new_widget_states}")
        if new_widget_states is not None:
            self.widget_states.update(new_widget_states)
        await self.run_script()

    @contextmanager
    def _redirect_stdout(self):
        """Capture stdout to send to the frontend"""
        logger.debug("Setting up stdout redirection")
        class PreswaldOutputStream:
            def __init__(self, callback):
                self.callback = callback

            def write(self, text):
                if text.strip():
                    logger.debug(f"Captured output: {text}")
                    asyncio.create_task(self.callback({
                        "type": "output",
                        "content": text
                    }))

            def flush(self):
                pass

        old_stdout = sys.stdout
        sys.stdout = PreswaldOutputStream(self.send_message)
        try:
            yield
        finally:
            sys.stdout = old_stdout
            logger.debug("Restored original stdout")

    async def run_script(self):
        """Execute the script and handle any deltas generated"""
        if not self._is_running or not self.script_path:
            logger.warning("Script runner not running or no script path set")
            return

        logger.info(f"Running script: {self.script_path}")
        
        # Set up the script execution environment
        script_globals = {
            "session_state": self.session_state,
            "widget_states": self.widget_states,
        }

        try:
            # Clear any existing components before running the script
            from preswald.core import _rendered_html
            _rendered_html.clear()
            logger.debug("Cleared existing components before script execution")

            # Capture script output
            with self._redirect_stdout():
                # Execute the script
                with open(self.script_path, "r") as f:
                    code = compile(f.read(), self.script_path, "exec")
                    logger.debug("Script compiled successfully")
                    exec(code, script_globals)
                    logger.debug("Script executed successfully")

                # Get rendered components
                from preswald.core import get_rendered_components
                components = get_rendered_components()
                logger.info(f"Rendered {len(components)} components")

                try:
                    # Send components to frontend
                    await self.send_message({
                        "type": "components",
                        "components": components
                    })
                except Exception as send_error:
                    logger.error(f"Error sending components to frontend: {send_error}", exc_info=True)

        except Exception as e:
            error_msg = f"Error executing script: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            try:
                await self.send_message({
                    "type": "error",
                    "content": {
                        "message": str(e),
                        "stack_trace": traceback.format_exc(),
                    },
                })
            except Exception as send_error:
                logger.error(f"Error sending error message to frontend: {send_error}", exc_info=True)
