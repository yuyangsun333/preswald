import toml

DEFAULT_THEME = {
    "color": {
        "primary": "#4CAF50",   # Default green for primary buttons/headers
        "secondary": "#FFC107",  # Default yellow for secondary elements
        "background": "#FFFFFF",  # Default white background
        "text": "#000000"       # Default black text color
    },
    "font": {
        "family": "Arial, sans-serif",  # Default font family
        "size": "16px"                # Default font size
    },
    "layout": {
        "sidebar_width": "250px"  # Default sidebar width
    }
}


def load_theme(config_path="config.toml"):
    """
    Load the theming configuration from a TOML file.

    Args:
        config_path (str): Path to the configuration TOML file.
    Returns:
        dict: Theming settings merged with defaults.
    """
    try:
        # Load the configuration file
        config = toml.load(config_path)
        print(f"Loaded config: {config}")
        theme = config.get("theme", {})
        # Merge with defaults to ensure all keys exist
        return merge_dicts(DEFAULT_THEME, theme)
    except FileNotFoundError:
        print(f"Config file '{config_path}' not found. Using default theme.")
        return DEFAULT_THEME
    except toml.TomlDecodeError as e:
        print(f"Error parsing config file: {e}. Using default theme.")
        return DEFAULT_THEME


def merge_dicts(defaults, custom):
    """
    Merge a custom dictionary into a default dictionary recursively.

    Args:
        defaults (dict): Default dictionary.
        custom (dict): Custom dictionary to merge into defaults.
    Returns:
        dict: Merged dictionary.
    """
    result = defaults.copy()
    for key, value in custom.items():
        if isinstance(value, dict) and key in result:
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def generate_css(theme):
    """
    Generate CSS styles based on the theming settings.

    Args:
        theme (dict): Theming configuration dictionary.
    Returns:
        str: CSS styles as a string.
    """
    color = theme.get("color", {})
    font = theme.get("font", {})
    layout = theme.get("layout", {})

    return f"""
    body {{
        background-color: {color.get("background")};
        color: {color.get("text")};
        font-family: {font.get("family")};
        font-size: {font.get("size")};
    }}
    .topbar {{
        background-color: {color.get("primary")};
        color: {color.get("text")};
        padding: 10px;
        text-align: center;
    }}
    .sidebar {{
        width: {layout.get("sidebar_width")};
        background-color: {color.get("secondary")};
        padding: 10px;
        float: left;
    }}
    .content {{
        margin-left: {layout.get("sidebar_width")};
        padding: 20px;
    }}
    .button {{
        background-color: {color.get("primary")};
        color: white;
        border: none;
        padding: 10px 20px;
        cursor: pointer;
    }}
    .button:hover {{
        background-color: {color.get("secondary")};
    }}
    """
