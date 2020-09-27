import logging
import time

from logging.handlers import RotatingFileHandler

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
#f_handler = logging.FileHandler('file.log')
f_handler = RotatingFileHandler('file.log', maxBytes=20,
                                  backupCount=5)
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

logger.warning('This is a warning')
logger.error('This is an error')

for i in range(100):
    logger.info("This is test log line %s" % i)
    time.sleep(0.25)