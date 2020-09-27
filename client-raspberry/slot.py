from datetime import datetime
import time
from log import *

class slot:
    isSlotStarted = False
    isStopSlot = False
    def __init__(self,onComplete ):
        logger.info(u"[Slot] Slot created")
        self.onComplete = onComplete
        self.startTime = datetime.now()
        self.schedulerStartTime = datetime.now()

    def startSlot(self, duration):
        if self.isSlotStarted : 
            logger.info(u"[Slot] Slot already started, ignored current request")
            return
        if(self.isStopSlot) :
            logger.info(u"[Slot] isStopSlot is ON, turn off this flag to start new slot")
            return
        self.isSlotStarted = True
        self.startTime = datetime.now()
        logger.info(u"[Slot]  Slot started for duration {}".format(duration))
        while(True and not self.isStopSlot):
            timeDiff = (datetime.now() - self.startTime).seconds
            if timeDiff < duration :
                time.sleep(1)
            else :
                break
        self.isSlotStarted = False
        logger.info(u"[Slot] Slot ended")
        self.onComplete(duration)

    def schedule(self, duration, callback):
        logger.info(u"[Slot] Scheduler started for {}".format(duration))
        self.schedulerStartTime = datetime.now()
        while(True):
            timeDiff = (datetime.now() - self.schedulerStartTime).seconds
            if timeDiff < duration :
                time.sleep(1)
            else :
                break
        logger.info(u"[Slot] Scheduler Ended for {}".format(duration))
        callback()

        
        

