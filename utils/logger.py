import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(log_file: str | None = None, level: int = logging.INFO):
    """Configure root logger to write to a rotating file and stream to stdout.

    - log_file: path to log file. If None, defaults to ../logs/app.log inside project.
    - level: logging level (default INFO).
    Returns the root logger instance.
    """
    # default log file inside project/logs/app.log
    if log_file is None:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        log_dir = os.path.join(base_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "app.log")

    # Create parent dir if needed
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(level)

    # remove existing handlers to avoid duplicate logs when re-initializing
    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")

    # File handler (rotating)
    fh = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Stream handler (stdout) for interactive runs
    sh = logging.StreamHandler()
    sh.setLevel(level)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    return logger
