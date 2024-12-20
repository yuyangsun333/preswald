import uuid


def generate_id(prefix="component"):
    """
    Generate a unique ID for a component.

    Args:
        prefix (str): Prefix for the component ID.
    Returns:
        str: A unique ID string.
    """
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def checkbox(label, default=False):
    """
    Create an HTML checkbox component.

    Args:
        label (str): Label for the checkbox.
        default (bool): Whether the checkbox is checked by default.
    Returns:
        str: HTML string for the checkbox.
    """
    checked = "checked" if default else ""
    id = generate_id("checkbox")
    return f'<input type="checkbox" id="{id}" {checked}> <label for="{id}">{label}</label>'


def slider(label, min_val=0, max_val=100, step=1, default=50):
    """
    Create an HTML slider component.

    Args:
        label (str): Label for the slider.
        min_val (int): Minimum value for the slider.
        max_val (int): Maximum value for the slider.
        step (int): Step size for the slider.
        default (int): Default value for the slider.
    Returns:
        str: HTML string for the slider.
    """
    id = generate_id("slider")
    return f"""
    <label for="{id}">{label}</label>
    <input type="range" id="{id}" name="{id}" min="{min_val}" max="{max_val}" step="{step}" value="{default}">
    """


def button(label):
    """
    Create an HTML button component.

    Args:
        label (str): Label for the button.
    Returns:
        str: HTML string for the button.
    """
    id = generate_id("button")
    return f'<button id="{id}">{label}</button>'


def selectbox(label, options, default=None):
    """
    Create an HTML select (dropdown) component.

    Args:
        label (str): Label for the dropdown.
        options (list): List of options for the dropdown.
        default (str): Default selected option.
    Returns:
        str: HTML string for the dropdown.
    """
    id = generate_id("selectbox")
    options_html = "".join(
        f'<option value="{opt}" {"selected" if opt ==
                                 default else ""}>{opt}</option>'
        for opt in options
    )
    return f"""
    <label for="{id}">{label}</label>
    <select id="{id}" name="{id}">
        {options_html}
    </select>
    """


def text_input(label, placeholder=""):
    """
    Create an HTML text input component.

    Args:
        label (str): Label for the text input.
        placeholder (str): Placeholder text for the input field.
    Returns:
        str: HTML string for the text input.
    """
    id = generate_id("textinput")
    return f"""
    <label for="{id}">{label}</label>
    <input type="text" id="{id}" name="{id}" placeholder="{placeholder}">
    """


def progress(label, value=0):
    """
    Create an HTML progress bar component.

    Args:
        label (str): Label for the progress bar.
        value (int): Current progress value (0-100).
    Returns:
        str: HTML string for the progress bar.
    """
    id = generate_id("progress")
    return f"""
    <label for="{id}">{label}</label>
    <progress id="{id}" value="{value}" max="100"></progress>
    """


def spinner(label):
    """
    Create an HTML spinner component.

    Args:
        label (str): Label for the spinner.
    Returns:
        str: HTML string for the spinner.
    """
    id = generate_id("spinner")
    return f"""
    <div id="{id}" class="spinner">
        <label>{label}</label>
        <div class="spinner-border" role="status"></div>
    </div>
    """


def alert(message, level="info"):
    """
    Create an HTML alert component.

    Args:
        message (str): Message for the alert.
        level (str): Alert level ('info', 'warning', 'error', 'success').
    Returns:
        str: HTML string for the alert.
    """
    level_class = {
        "info": "alert-info",
        "warning": "alert-warning",
        "error": "alert-danger",
        "success": "alert-success",
    }.get(level, "alert-info")
    id = generate_id("alert")
    return f'<div id="{id}" class="alert {level_class}">{message}</div>'


def image(src, alt="Image"):
    """
    Create an HTML image component.

    Args:
        src (str): Source URL for the image.
        alt (str): Alternate text for the image.
    Returns:
        str: HTML string for the image.
    """
    id = generate_id("image")
    return f'<img id="{id}" src="{src}" alt="{alt}" style="max-width: 100%; height: auto;">'
