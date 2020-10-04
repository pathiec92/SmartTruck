import subprocess
import signal
import os
from log import *
from slot import *
import threading

from datetime import datetime as dt

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
        
diag = DiagService()
diag.startProcess()