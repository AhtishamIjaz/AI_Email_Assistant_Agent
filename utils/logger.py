import logging
import sys

def setup_logger(name: str):
    """Sets up a professional logger with a specific format."""
    
    # 1. Create a logger instance
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 2. Define the format (Time - Name - Level - Message)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 3. Console Handler (Shows logs in your terminal)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # 4. File Handler (Saves logs to a file called 'app.log')
    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(formatter)

    # Avoid duplicate logs if the logger is already set up
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# Create a default logger for the project
logger = setup_logger("EmailAgent")