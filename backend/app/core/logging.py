import sys

from loguru import logger


logger.remove()

logger.add(
    sys.stdout,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:"
        "<cyan>{line}</cyan> - <level>{message}</level>"
    ),
    level="INFO",
    colorize=True,
)

logger.add(
    "logs/predictamaint.log",
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    level="INFO",
)

app_logger = logger