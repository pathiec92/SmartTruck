from pyimagesearch.utils import Conf
import argparse
from slot import *
from datetime import datetime
import threading
from record import *
from repo import *
from util import currentSlot
from offline import removeDir
from log import *

#import sched, time
SESSION_BUFFER = 20
class session:
    # sessions: 10, 20,40,80,160,320,640...
    session_num = 10
    expo = 2
    isDetected = False
    isSessionStarted = False
    isSlotRunning = False
    rcd = record()
    isSendMessage = False
        
    def __init__(self, onSessionComplete, fservice):
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        logger.info(str(ap))
        ap.add_argument("-c", "--conf", required=True,help="Path to the input configuration file")
        ap.add_argument("-dv", "--delv",  action="store_true", help="Delete Video cache (Y/N)")
        args = vars(ap.parse_args())
        logger.info(u"[session] Args1 are {}".format(args))
        if args["delv"]:
            logger.info("Delete video cache!")
            removeDir(".vcache")
            removeDir(".vLinks")

        self.slt = slot(self.onSlotComplete)
        self.conf = Conf(args["conf"])
        self.session_duration = self.conf["session_duration"] + SESSION_BUFFER
        self.onSessionComplete = onSessionComplete
        self.cloud = Gcloud(self.conf, fservice)
        self.fservice = fservice
        #self.scheduler = sched.scheduler(time.time, time.sleep)
        logger.info(u"[Session] duration = {}".format(str(self.session_duration )))

    def startSession(self,frame):
        if self.isSessionStarted : 
            logger.info(u"[Session] Session already started, ignored current request")
            return
        logger.info(u"[Session] NEW SESSION STARTED @ {}".format(datetime.now()))
        self.fservice.uploadEvent("Attention! Detected Human inside the truck", "warning")

        t= threading.Thread(target=self.slt.schedule,args=(self.session_duration, self.sessionCompleted))
        t.start()
        logger.info(u"[Session] Started scheduler for duration {}".format(self.session_duration))
        self.session_num = 5
        self.isSessionStarted = True
        self.session_num = self.session_num * self.expo
        self.startSlot(self.session_num,frame)
        self.isSendMessage = False


    def startSlot(self,duration,frame):
        self.rcd.startRecord(frame)
        self.isSlotRunning = True
        self.isSendMessage = False
        currentSlot = duration
        logger.info(u"[Session] Starting slot for duration = {}".format(duration))
        logger.info(u"[Session] SLOT STARTED @ {}".format(datetime.now()))
        self.slt.isStopSlot = False
        t= threading.Thread(target=self.slt.startSlot,args=(duration,))
        t.start()

    def humanDetected(self,frame):
        self.isDetected = True
        self.startNewSlotIfNot(frame)
    
    def captureFrames(self, frame):
        if(self.isDetected):
           # logger.info("Capturing the frame")
            self.startNewSlotIfNot(frame)

    def startNewSlotIfNot(self,frame):
        if(self.isSlotRunning):
            self.rcd.recordFrame(frame)
            #logger.info("slot is running already, just record the frame")
            return
        if self.isSessionStarted :
            self.startSlot(self.session_num, frame)
        else:
            self.startSession(frame)
            

    def onSlotComplete(self, duration):
        self.endSlot()
        logger.info(u"[Session] Slot completed for duration {}".format(duration))
        self.session_num = self.session_num *  self.expo
        self.isDetected = False
        self.isSlotRunning = False
        self.isSendMessage = False
        logger.info(u"[Session] SLOT COMPLETED @ {}".format(datetime.now()))

    def sessionCompleted(self):
        logger.info(u"[Session] SESSION COMPLETED @ {}".format(datetime.now()))
        self.isSessionStarted = False
        self.slt.isStopSlot = True
        self.onSessionComplete()

    def endSlot(self):
        self.rcd.stopRecord()

        t= threading.Thread(target=self.cloud.upload,args=(self.rcd.tempVideo,self.isSendMessage))
        t.start()
        #logger.info(u"downloadPath = {}".format(downloadPath))



        
        


