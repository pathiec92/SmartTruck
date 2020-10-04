import sys
import cv2
from imutils.io import TempFile
from datetime import datetime
import os   
from offline import createDir
from log import *

class record :
    def __init__(self):
        self.startTime = datetime.now()
        self.writer = None
        self.tempVideo = None
        self.vcache = createDir('.vcache')

    def startRecord(self, frame):
        (H, W) = frame.shape[:2]
        self.startTime = datetime.now()
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.tempVideo = TempFile(basePath=self.vcache, ext=".mp4")
        self.writer = cv2.VideoWriter(self.tempVideo.path, fourcc, 30, (W, H),True)
        logger.info(u"Start recording, now = " + str(self.startTime))
          

    def recordFrame(self,frame):
        if self.tempVideo is None or self.writer is None:
            logger.info(u"Video record is not started yet.")
            return
        self.writer.write(frame)

    def stopRecord(self):
        self.writer.release()
        self.writer = None
        logger.info(u"Time out, stop recording, upload and send sms")