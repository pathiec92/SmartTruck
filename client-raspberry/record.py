import sys
import cv2
from imutils.io import TempFile
from datetime import datetime

class record :
    def __init__(self):
        self.startTime = datetime.now()
        self.writer = None
        self.tempVideo = None

    def startRecord(self, frame):
        (H, W) = frame.shape[:2]
        self.startTime = datetime.now()
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.tempVideo = TempFile(basePath="/home/zebra/PythonHome/DetectRecordSend", ext=".mp4")
        self.writer = cv2.VideoWriter(self.tempVideo.path, fourcc, 30, (W, H),True)
        print("Start recording, now = " + str(self.startTime))
          

    def recordFrame(self,frame):
        if self.tempVideo is None or self.writer is None:
            print("Video record is not started yet.")
            return
        self.writer.write(frame)

    def stopRecord(self):
        self.writer.release()
        self.writer = None
        print("Time out, stop recording, upload and send sms")