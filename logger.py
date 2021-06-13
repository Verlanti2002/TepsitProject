import logging
import os


def get_logger(create_file=False, filename="main.log"):
    # create logger for prd_ci
    log = logging.getLogger(__name__)
    log.setLevel(level=logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s - %(levelname)s - %(message)s')

    if create_file:
        if not os.path.exists("log"):
            os.makedirs("log")
        # create file handler for logger.
        file_handler = logging.FileHandler(os.path.join("log", filename))
        file_handler.setLevel(level=logging.DEBUG)
        file_handler.setFormatter(formatter)

    # create console handler for logger.
    ch = logging.StreamHandler()
    ch.setLevel(level=logging.DEBUG)
    ch.setFormatter(formatter)

    # add handlers to logger.
    if create_file:
        log.addHandler(file_handler)
    log.addHandler(ch)
    return log

