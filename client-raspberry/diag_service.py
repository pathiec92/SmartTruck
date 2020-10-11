import subprocess
import signal
import os
from log import *
from slot import *
import threading
from firestore_service import *
import time
from datetime import datetime as dt
import argparse
from pyimagesearch.utils import Conf

class DiagService:
    def __init__(self ):
        logger.info(u"[DiagService] created")
        self.slt = slot(self.onSlotComplete)
    def onSlotComplete(self, duration):
        print('slot completed')
        self.stopProcess("human_detect")

    def sessionCompleted(self):
        print(u"[Session] SESSION COMPLETED @ {}".format(datetime.now()))
        self.startProcess()
        self.stopProcess("human_detect")
        

    def startProcess(self):
        t= threading.Thread(target=self.slt.schedule,args=(20, self.sessionCompleted))
        t.start()

    def stopProcess(self, grep):
        os.system('ps axf | grep human_detect | grep -v grep | awk \'{print \"kill -9 \" $1}\' | sh')
        print('Starting human-detection')
        os.system('cd /home/zebra/SmartTruck/client-raspberry; python3 human_detect.py -c config/config.json')
        
#diag = DiagService()
#diag.startProcess()

#subscribe for ActiveLoad
# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-c", "--conf", required=True,
# 	help="Path to the input configuration file")
# ap.add_argument("-dv", "--delv",  action="store_true",
# 	help="Delete Video cache (Y/N)")
# args = vars(ap.parse_args())
# logger.info(u"Args1 are {}".format(args))

# # load the configuration file and initialize the Twilio notifier
# conf = Conf(args["conf"])
# truckId = conf["truckId"]

fireStoreService = FireStoreService()
fireStoreService.subscribeCommand()
fireStoreService.publishDeviceId()
while True:
    time.sleep(0.1)
