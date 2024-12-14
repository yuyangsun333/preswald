import logging

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

def log_message(level, message):
    """
    Log a message at the specified log level.
    
    Args:
        level (str): The log level ('info', 'warning', 'error', etc.).
        message (str): The message to log.
    
    Returns:
        None
    """
    log_levels = {
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "debug": logging.DEBUG,
    }
    if level in log_levels:
        logging.log(log_levels[level], message)
    else:
        logging.error(f"Unsupported log level: {level}")
