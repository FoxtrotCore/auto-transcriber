from datetime import datetime as dt
from logging import (
    DEBUG,
    INFO,
    FileHandler,
    Formatter,
    Logger,
    StreamHandler,
    getLogger,
)
from pathlib import Path

from . import APP_NAME


def get_logger(log_name: str = APP_NAME, verbose: bool = False) -> Logger:
    now = dt.now().isoformat().replace(":", "-").replace("T", "_").split(".")[0]
    logger = getLogger(log_name)

    if getattr(logger, "_configured", False):
        return logger

    log_level = DEBUG if verbose else INFO
    logger.setLevel(log_level)
    logger.propagate = False

    stream_handler = StreamHandler()
    stream_handler.setLevel(log_level)

    file_handler = FileHandler(Path(f"./{now}-ftf-auto-transcriber.log").absolute())
    file_handler.setLevel(log_level)

    formatter = Formatter(fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s")
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger._configured = True
    return logger
