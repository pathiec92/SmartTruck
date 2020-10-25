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
        self.fireStoreService = FireStoreService()
        self.fireStoreService.instance = 'diag'
        print('publishing device id')
        self.fireStoreService.publishDeviceId()

    def onSlotComplete(self, duration):
        print('heart beat timeOUt')
        self.stopProcess("human_detect")

    def sessionCompleted(self):
        print(u"[DiagService] Sending HEART BEAT @ {}".format(datetime.now()))
        self.fireStoreService.publishDeviceId()
        self.startProcess()
        #self.stopProcess("human_detect")
    
    def startHeartBeat(self):
        self.startProcess()

    def startProcess(self):
        t= threading.Thread(target=self.slt.schedule,args=(120, self.sessionCompleted))
        t.start()

    def stopProcess(self, grep):
        os.system('ps axf | grep human_detect | grep -v grep | awk \'{print \"kill -9 \" $1}\' | sh')
        print('Starting human-detection')
#		os.system('cd /home/satyol/cambot; python3 human_detect.cpython-37.pyc -c config/config.json')
        os.system('cd ~/SmartTruck/client-raspberry; python3 human_detect.py -c config/config.json')
        
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



diag = DiagService()

diag.startHeartBeat()
while True:
    time.sleep(0.1)
