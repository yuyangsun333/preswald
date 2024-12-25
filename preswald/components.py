import uuid
from preswald.core import _rendered_html, get_component_state
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def generate_id(prefix="component"):
    """Generate a unique ID for a component."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"

def checkbox(label, default=False):
    """Create a checkbox component."""
    id = generate_id("checkbox")
    logger.debug(f"Creating checkbox component with id {id}, label: {label}")
    component = {
        "type": "checkbox",
        "id": id,
        "label": label,
        "value": get_component_state(id, default)
    }
    logger.debug(f"Created component: {component}")
    _rendered_html.append(component)
    return component

def slider(label, min_val=0, max_val=100, step=1, default=50):
    """Create a slider component."""
    id = generate_id("slider")
    logger.debug(f"Creating slider component with id {id}, label: {label}")
    component = {
        "type": "slider",
        "id": id,
        "label": label,
        "min": min_val,
        "max": max_val,
        "step": step,
        "value": get_component_state(id, default)
    }
    logger.debug(f"Created component: {component}")
    _rendered_html.append(component)
    return component

def button(label):
    """Create a button component."""
    id = generate_id("button")
    logger.debug(f"Creating button component with id {id}, label: {label}")
    component = {
        "type": "button",
        "id": id,
        "label": label
    }
    logger.debug(f"Created component: {component}")
    _rendered_html.append(component)
    return component

def selectbox(label, options, default=None):
    """Create a select component."""
    id = generate_id("selectbox")
    logger.debug(f"Creating selectbox component with id {id}, label: {label}")
    component = {
        "type": "selectbox",
        "id": id,
        "label": label,
        "options": options,
        "value": get_component_state(id, default or options[0] if options else None)
    }
    logger.debug(f"Created component: {component}")
    _rendered_html.append(component)
    return component

def text_input(label, placeholder=""):
    """Create a text input component."""
    id = generate_id("text_input")
    logger.debug(f"Creating text input component with id {id}, label: {label}")
    component = {
        "type": "text_input",
        "id": id,
        "label": label,
        "placeholder": placeholder,
        "value": get_component_state(id, "")
    }
    logger.debug(f"Created component: {component}")
    _rendered_html.append(component)
    return component

def progress(label, value=0):
    """Create a progress component."""
    id = generate_id("progress")
    logger.debug(f"Creating progress component with id {id}, label: {label}")
    component = {
        "type": "progress",
        "id": id,
        "label": label,
        "value": value
    }
    logger.debug(f"Created component: {component}")
    _rendered_html.append(component)
    return component

def spinner(label):
    """Create a spinner component."""
    id = generate_id("spinner")
    logger.debug(f"Creating spinner component with id {id}, label: {label}")
    component = {
        "type": "spinner",
        "id": id,
        "label": label
    }
    logger.debug(f"Created component: {component}")
    _rendered_html.append(component)
    return component

def alert(message, level="info"):
    """Create an alert component."""
    id = generate_id("alert")
    logger.debug(f"Creating alert component with id {id}, message: {message}")
    component = {
        "type": "alert",
        "id": id,
        "message": message,
        "level": level
    }
    logger.debug(f"Created component: {component}")
    _rendered_html.append(component)
    return component

def image(src, alt="Image"):
    """Create an image component."""
    id = generate_id("image")
    logger.debug(f"Creating image component with id {id}, src: {src}")
    component = {
        "type": "image",
        "id": id,
        "src": src,
        "alt": alt
    }
    logger.debug(f"Created component: {component}")
    _rendered_html.append(component)
    return component

def text(markdown_str):
    """Create a text/markdown component."""
    id = generate_id("text")
    logger.debug(f"Creating text component with id {id}")
    component = {
        "type": "text",
        "id": id,
        "markdown": markdown_str,
        "value": markdown_str
    }
    logger.debug(f"Created component: {component}")
    _rendered_html.append(component)
    return component
