from loguru import logger

logger.add("transactions-api.log", rotation="500 MB", retention="20 days")
