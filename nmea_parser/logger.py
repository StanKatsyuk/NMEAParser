import os
import logging

from config import Config


def get_logger():
    return logging.getLogger()


def setup_logger():
    # Configure global logger
    if not os.path.isdir(Config.log_dir):
        os.mkdir(Config.log_dir)

    logger = logging.getLogger()
    logger.setLevel(Config.logging_level)
    logging.getLogger('matplotlib.font_manager').disabled = True  # Turns off logging for useless
    file_handler = logging.FileHandler(Config.log_filepath)
    formatter = logging.Formatter(Config.log_format)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return get_logger()
