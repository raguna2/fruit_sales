import logging
def info(msg):
    logger = logging.getLogger('command')
    logger.info(msg)
