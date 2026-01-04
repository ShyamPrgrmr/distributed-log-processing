import logging
import sys

def normal_app_logger(name="app"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-5s %(process)d --- "
        "[%(threadName)s] %(name)s : %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S.%f"
    )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.propagate = False
    return logger