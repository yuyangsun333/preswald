import sys
from typing import Dict, Callable, Optional
from contextlib import contextmanager
import traceback


class ScriptRunner:
    def __init__(self, session_id: str, send_message_callback: Callable):
        self.session_id = session_id
        self.send_message = send_message_callback
        self.script_path: Optional[str] = None
        self.widget_states: Dict = {}
        self._is_running = False

        # Store for session state
        self.session_state = {}

    async def start(self, script_path: str = "app.py"):
        """Start running the script"""
        self.script_path = script_path
        self._is_running = True
        await self.run_script()

    async def stop(self):
        """Stop the script runner"""
        self._is_running = False

    async def rerun(self, new_widget_states: Dict = None):
        """Rerun the script with potentially new widget values"""
        if new_widget_states is not None:
            self.widget_states.update(new_widget_states)
        await self.run_script()

    @contextmanager
    def _redirect_stdout(self):
        """Capture stdout to send to the frontend"""

        class PreswaldOutputStream:
            def __init__(self, callback):
                self.callback = callback

            def write(self, text):
                if text.strip():  # Only send non-empty text
                    # We immediately send each piece of text - no buffering
                    self.callback({"type": "text", "content": text})

            def flush(self):
                # No buffering is done, so flush is a no-op
                # We implement it only to satisfy the file-like object interface
                pass

        old_stdout = sys.stdout
        sys.stdout = PreswaldOutputStream(self.send_message)
        try:
            yield
        finally:
            sys.stdout = old_stdout

    async def run_script(self):
        """Execute the script and handle any deltas generated"""
        if not self._is_running or not self.script_path:
            return

        # Set up the script execution environment
        script_globals = {
            "session_state": self.session_state,
            "widget_states": self.widget_states,
            "send_delta": self.send_message,
        }

        try:
            # Capture script output
            with self._redirect_stdout():
                # Execute the script
                with open(self.script_path, "r") as f:
                    code = compile(f.read(), self.script_path, "exec")
                    exec(code, script_globals)

        except Exception as e:
            # Send error message to frontend
            await self.send_message(
                {
                    "type": "error",
                    "content": {
                        "message": str(e),
                        "stack_trace": traceback.format_exc(),
                    },
                }
            )
