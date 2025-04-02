import logging
import sys


def setup_logging() -> None:
    """
    Set up logging configuration for the application.
    """
    log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)
    
    # Loggers for each specific part of our API
    loggers = {
        "fastapi": logging.INFO,
        "uvicorn": logging.INFO,
        "app": logging.DEBUG,
    }
    
    # Set levels
    for logger_name, log_level in loggers.items():
        module_logger = logging.getLogger(logger_name)
        module_logger.setLevel(log_level)
        module_logger.propagate = True


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.
    
    Args:
        name (str): The name of the module
        
    Returns:
        logging.Logger: The configured logger
    """
    return logging.getLogger(name)