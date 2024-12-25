import sys
import traceback
import logging
from contextlib import contextmanager
from typing import Dict, Callable, Optional
import asyncio
from preswald.core import update_component_state, get_component_state, get_all_component_states

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ScriptRunner:
    def __init__(self, session_id: str, send_message_callback: Callable, initial_states: Dict = None):
        self.session_id = session_id
        self.send_message = send_message_callback
        self.script_path: Optional[str] = None
        self.widget_states = initial_states or {}
        self._is_running = False
        self.session_state = {}
        logger.info(f"[ScriptRunner] Initialized with session_id: {session_id}")
        if initial_states:
            logger.info(f"[ScriptRunner] Loaded initial states: {initial_states}")

    async def start(self, script_path: str = "app.py"):
        """Start running the script"""
        logger.info(f"[ScriptRunner] Starting execution: {script_path}")
        self.script_path = script_path
        self._is_running = True
        
        # Initialize core states from widget states
        for component_id, value in self.widget_states.items():
            update_component_state(component_id, value)
            logger.debug(f"[ScriptRunner] Initialized state: {component_id} = {value}")
        
        await self.run_script()

    async def stop(self):
        """Stop the script runner"""
        logger.info("[ScriptRunner] Stopping")
        self._is_running = False

    async def rerun(self, new_widget_states: Dict = None):
        """Rerun the script with potentially new widget values"""
        if not new_widget_states:
            logger.debug("[ScriptRunner] No new states for rerun")
            return

        logger.info(f"[ScriptRunner] Rerunning with new states: {new_widget_states}")
        
        # Update both widget and core states
        for component_id, value in new_widget_states.items():
            try:
                old_value = self.widget_states.get(component_id)
                self.widget_states[component_id] = value
                update_component_state(component_id, value)
                logger.debug(f"[ScriptRunner] Updated state: {component_id} = {value} (was {old_value})")
            except Exception as e:
                logger.error(f"[ScriptRunner] Error updating state for {component_id}: {e}")
        
        await self.run_script()

    @contextmanager
    def _redirect_stdout(self):
        """Capture stdout to send to the frontend"""
        logger.debug("[ScriptRunner] Setting up stdout redirection")
        class PreswaldOutputStream:
            def __init__(self, callback):
                self.callback = callback
                self.buffer = ""

            def write(self, text):
                self.buffer += text
                if "\n" in self.buffer:
                    lines = self.buffer.split("\n")
                    for line in lines[:-1]:
                        if line.strip():
                            logger.debug(f"[ScriptRunner] Captured output: {line}")
                            asyncio.create_task(self.callback({
                                "type": "output",
                                "content": line + "\n"
                            }))
                    self.buffer = lines[-1]

            def flush(self):
                if self.buffer:
                    if self.buffer.strip():
                        logger.debug(f"[ScriptRunner] Flushing output: {self.buffer}")
                        asyncio.create_task(self.callback({
                            "type": "output",
                            "content": self.buffer
                        }))
                    self.buffer = ""

        old_stdout = sys.stdout
        sys.stdout = PreswaldOutputStream(self.send_message)
        try:
            yield
        finally:
            sys.stdout.flush()
            sys.stdout = old_stdout
            logger.debug("[ScriptRunner] Restored stdout")

    async def run_script(self):
        """Execute the script and handle any deltas generated"""
        if not self._is_running or not self.script_path:
            logger.warning("[ScriptRunner] Not running or no script path set")
            return

        logger.info(f"[ScriptRunner] Running script: {self.script_path}")
        
        # Set up the script execution environment
        script_globals = {
            "session_state": self.session_state,
            "widget_states": self.widget_states,
        }

        try:
            # Import core components
            from preswald.core import _rendered_html, get_rendered_components
            
            # Only clear components if this is not a rerun with existing components
            if not _rendered_html:
                logger.debug("[ScriptRunner] No existing components, proceeding with script execution")
            else:
                logger.debug(f"[ScriptRunner] Found {len(_rendered_html)} existing components")

            # Capture script output
            with self._redirect_stdout():
                # Execute the script
                with open(self.script_path, "r") as f:
                    code = compile(f.read(), self.script_path, "exec")
                    logger.debug("[ScriptRunner] Script compiled")
                    exec(code, script_globals)
                    logger.debug("[ScriptRunner] Script executed")

                # Get rendered components
                components = get_rendered_components()
                logger.info(f"[ScriptRunner] Rendered {len(components)} components")

                if components:  # Only process if we have components
                    # Update components with current states
                    for component in components:
                        if 'id' in component:
                            # First check widget states, then fall back to core state
                            current_state = self.widget_states.get(
                                component['id'],
                                get_component_state(component['id'])
                            )
                            if current_state is not None and 'value' in component:
                                component['value'] = current_state
                                logger.debug(f"[ScriptRunner] Set component {component['id']} value: {current_state}")

                    try:
                        # Send components to frontend only if we have components
                        await self.send_message({
                            "type": "components",
                            "components": components
                        })
                        logger.debug("[ScriptRunner] Sent components to frontend")
                    except Exception as send_error:
                        logger.error(f"[ScriptRunner] Error sending components: {send_error}", exc_info=True)
                        raise

        except Exception as e:
            error_msg = f"Error executing script: {str(e)}\n{traceback.format_exc()}"
            logger.error(f"[ScriptRunner] {error_msg}")
            try:
                await self.send_message({
                    "type": "error",
                    "content": {
                        "message": str(e),
                        "stack_trace": traceback.format_exc(),
                    },
                })
            except Exception as send_error:
                logger.error(f"[ScriptRunner] Error sending error message: {send_error}", exc_info=True)
