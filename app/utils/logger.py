import logging
import os
from logging.handlers import RotatingFileHandler


# Create logs folder if it doesn't exist
os.makedirs("logs", exist_ok=True)


logger = logging.getLogger("mymovielist")
logger.setLevel(logging.INFO)

# Prevent duplicate logs if the module is imported multiple times
if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # File Handler (for local development)
    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=5_000_000,
        backupCount=5,
    )
    file_handler.setFormatter(formatter)

    # Console Handler (for Railway and terminal)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Add both handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)