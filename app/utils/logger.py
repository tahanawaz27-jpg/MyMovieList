import logging
import os
from logging.handlers import RotatingFileHandler


# Create logs folder if it doesn't exist
os.makedirs("logs", exist_ok=True)


logger = logging.getLogger("mymovielist")
logger.setLevel(logging.INFO)


# File handler
file_handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=5_000_000,
    backupCount=5
)


formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)