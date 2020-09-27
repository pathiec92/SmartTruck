import logging
import time
import os 

from logging.handlers import RotatingFileHandler

def createDir(folderName):
    path = ""
    current_directory = os.getcwd()
    path = os.path.join(current_directory, folderName)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

# Create a custom logger
logger = logging.getLogger(__name__)
print("logger {}", logger)

# Create handlers
#f_handler = logging.FileHandler('file.log')
path = createDir("logs")
print('log path {}', path)
f_handler = RotatingFileHandler('logs/smart_truck.log', maxBytes=10485760,
                                  backupCount=5)
f_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(f_handler)
logging.getLogger().setLevel(logging.DEBUG)
print("After setting logger {}", logger)
logger.info('This is Info')
logger.warning('This is a warning')
logger.error('This is an error')

