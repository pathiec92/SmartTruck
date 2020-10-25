import sys
import cv2
from imutils.io import TempFile
from datetime import datetime
import os   
from offline import createDir
from pyimagesearch.keyclipwriter import KeyClipWriter
from log import *

class record :
    #key clips before/affer buffer and codec
	#"keyclipwriter_buffersize": 50
    kcw = KeyClipWriter(bufSize=50)
    def __init__(self):
        self.startTime = datetime.now()
        self.writer = None
        self.tempVideo = None
        self.vcache = createDir('.vcache')

    def startRecord(self, frame):
        # (H, W) = frame.shape[:2]
        self.startTime = datetime.now()
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.tempVideo = TempFile(basePath=self.vcache, ext=".avi")
        self.kcw.start(self.tempVideo.path, fourcc, 16)
        logger.info(u"Start recording, now = " + str(self.startTime))
          

    def recordFrame(self,frame):
        timestamp = datetime.now()
         # draw the text and timestamp on the frame
        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.4, (255, 255, 0), 1)
        # cv2.imshow("Frame", frame)
        self.kcw.update(frame)

    def stopRecord(self):
        self.kcw.finish()
        self.writer = None
        logger.info(u"Time out, stop recording, upload and send sms")