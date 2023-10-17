# coding:utf-8
from loguru import logger

logger.add("./logs/interface_log_{time}.log", rotation="500MB", encoding="utf-8", enqueue=True, compression="zip", retention="10 days")
logger.info("中文test")
logger.info([1, "fdsfdsf", "测试"])
logger.debug("中文test")
logger.error("中文test")
logger.warning("中文test")