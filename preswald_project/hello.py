from preswald import text, checkbox, slider, button, selectbox, text_input, progress, spinner, alert, image
import time
import threading
import logging
from preswald.core import register_component_callback, get_component_state

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Store component values
component_values = {}

def handle_component_update(component_id, value):
    """Callback function to handle component updates"""
    old_value = component_values.get(component_id)
    component_values[component_id] = value
    logger.info(f"[Component Callback] State update for {component_id}:")
    logger.info(f"  - Old value: {old_value}")
    logger.info(f"  - New value: {value}")

def log_component_values():
    """Periodically log all component values"""
    while True:
        if component_values:
            logger.info("[Component States] Current values:")
            for component_id, value in component_values.items():
                # Get the latest value from the core state
                current_value = get_component_state(component_id, value)
                if current_value != value:
                    logger.warning(f"  - {component_id}: Value mismatch!")
                    logger.warning(f"    Local: {value}")
                    logger.warning(f"    Core:  {current_value}")
                else:
                    logger.info(f"  - {component_id}: {current_value}")
        time.sleep(10)  # Log every 5 seconds

# Start logging thread
logging_thread = threading.Thread(target=log_component_values, daemon=True)
logging_thread.start()

logger.info("[Script] Creating components...")

text("# Welcome to Preswald!")
text("This is your first app. 🎉")

# Create components and register callbacks for state updates
checkbox_comp = checkbox("Check me", default=False)
component_values[checkbox_comp['id']] = checkbox_comp['value']
register_component_callback(checkbox_comp['id'], lambda v: handle_component_update(checkbox_comp['id'], v))
logger.info(f"[Component Init] Checkbox created: {checkbox_comp['id']}")

slider_comp = slider("Adjust value", 0, 100, 25)
component_values[slider_comp['id']] = slider_comp['value']
register_component_callback(slider_comp['id'], lambda v: handle_component_update(slider_comp['id'], v))
logger.info(f"[Component Init] Slider created: {slider_comp['id']}")

button_comp = button("Click me")
component_values[button_comp['id']] = False
register_component_callback(button_comp['id'], lambda v: handle_component_update(button_comp['id'], v))
logger.info(f"[Component Init] Button created: {button_comp['id']}")

select_comp = selectbox("Select an option", ["Option 1", "Option 2", "Option 3"])
component_values[select_comp['id']] = select_comp['value']
register_component_callback(select_comp['id'], lambda v: handle_component_update(select_comp['id'], v))
logger.info(f"[Component Init] Selectbox created: {select_comp['id']}")

input_comp = text_input("Enter your name")
component_values[input_comp['id']] = input_comp['value']
register_component_callback(input_comp['id'], lambda v: handle_component_update(input_comp['id'], v))
logger.info(f"[Component Init] Text input created: {input_comp['id']}")

progress_comp = progress("Loading progress", 0.5)
component_values[progress_comp['id']] = progress_comp['value']
register_component_callback(progress_comp['id'], lambda v: handle_component_update(progress_comp['id'], v))
logger.info(f"[Component Init] Progress created: {progress_comp['id']}")

spinner("Loading...")
alert("This is an alert")
image("https://picsum.photos/200/300")

logger.info("[Script] All components created and initialized")
