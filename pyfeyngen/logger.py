import logging
# Main logger for the pyfeyngen package
logger = logging.getLogger('pyfeyngen')

def setup_logging(debug=False):
    """
    Configure the logger for pyfeyngen.
    If debug is True, set level to DEBUG and print debug activation message.
    Ensures only one handler is added.
    """
    level = logging.DEBUG if debug else logging.INFO
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    if debug:
        logger.debug("DEBUG mode activated")