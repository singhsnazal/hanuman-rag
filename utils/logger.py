import logging
import sys

def get_logger(name="hanuman_god"):
    logger = logging.getLogger(name)

    # Important: avoid adding handlers multiple times
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

        # prevents duplicate logs through root logger
        logger.propagate = False

    return logger
