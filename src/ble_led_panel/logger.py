import logging
import sys
from colorama import Fore, Style, init

# Initialize colorama for Windows support
init(autoreset=True)

# Define the longest log level label (container size)
MAX_LABEL_LENGTH = len("CRITICAL")  # The longest log level

# Create a custom formatter class
class CustomFormatter(logging.Formatter):
    """Custom formatter for color-coded log levels with equal-length labels."""
    
    # Define different log formats and colors for each level
    LOG_COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    LEVEL_LABELS = {
        logging.DEBUG: "DEBUG",
        logging.INFO: "INFO",
        logging.WARNING: "WARNING",
        logging.ERROR: "ERROR",
        logging.CRITICAL: "CRITICAL",
    }

    def format(self, record):
        # Get the color and label for the current log level
        log_color = self.LOG_COLORS.get(record.levelno, Fore.WHITE)
        label = self.LEVEL_LABELS.get(record.levelno, "LOG")

        # Calculate the padding to ensure all labels are of equal length
        # Padding is done to match the size of the longest label "CRITICAL"
        padded_label = f"[  {label.center(MAX_LABEL_LENGTH)} ]"

        # Define the format string with the color and padded label
        log_fmt = f"{log_color}{padded_label} %(message)s"
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Function to set up the logger
def setup_logger(name: str, level: int = logging.INFO):
    """Set up a logger with color output to the console."""
    logger = logging.getLogger(name)
    logger.setLevel(level)  # Set the logging level passed as an argument

    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Set the custom formatter for the console handler
    console_handler.setFormatter(CustomFormatter())

    # Add the handler to the logger if it hasn't been added already
    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    return logger