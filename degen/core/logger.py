import logging
import sys

LOGGER_NAME = "degen"

logger = logging.getLogger(LOGGER_NAME)


def configure_logger(verbose: bool = False, quiet: bool = False):
    """
    Configure logging behavior.

    verbose=True  -> DEBUG
    quiet=True    -> ERROR
    default       -> INFO
    """

    if verbose:
        level = logging.DEBUG
    elif quiet:
        level = logging.ERROR
    else:
        level = logging.INFO

    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)

    # Prevent duplicate handlers
    if not logger.handlers:
        logger.addHandler(handler)

    return logger