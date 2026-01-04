import logging
import os
import socket

from logging.handlers import RotatingFileHandler
from appLogger import normal_app_logger
from constants import *

normLogger = normal_app_logger()
container_id = socket.gethostname()
maxLogSize = (DEFAULT_MAX_LOG_SIZE * 1024 * 1024) if os.environ.get(MAX_LOG_SIZE)==None else (int(os.environ.get(MAX_LOG_SIZE)) * 1024 * 1024)
backupCount = DEFAULT_BACKUP_COUNT if os.environ.get(BACKUP_COUNT)==None else int(os.environ.get(BACKUP_COUNT))

normLogger.info("MAX LOG SIZE : {} Bytes".format(maxLogSize))
normLogger.info("BACKUP COUNT : {}".format(backupCount))


def setup_logger(component):
    logger = logging.getLogger(component)
    logger.setLevel(logging.INFO)

    log_path = f"{LOG_DIR}/{component}.{container_id}.log"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    handler = RotatingFileHandler(
        log_path,
        maxBytes=maxLogSize,
        backupCount=backupCount,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-5s %(process)d --- "
        "[%(threadName)s] %(name)s "
        "[traceId=%(traceId)s spanId=%(spanId)s "
        "paymentId=%(paymentId)s] : "
        "%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S.%f"
    )

    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    logger.propagate = False
    return logger



def getLogsPath(path:str):
    paths = path.split(",")
    return [path.strip() for path in paths]
