# core/logging_config.py

import logging

logging.basicConfig(
    level=logging.INFO,  # or logging.DEBUG
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("my-fastapi-app")
