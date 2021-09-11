import sys
import cv2
from imutils.io import TempFile
from repo import *

from datetime import datetime
# initialize the flags for fridge open and notification sent
class state:
    def __init__(self, conf, fservice):
        self.isRecording = False
        self.isNotificationSent = False
        self.isPrevRecording = False
        self.startTime = datetime.now()
        self.writer = None
        self.cloud = Gcloud( fservice)
        # self.W = None
        # self.H = None
        self.tempVideo = None
        self.fservice = fservice

    def recordIt(self,frame, conf):
        (H, W) = frame.shape[:2]
        print("isRecording = "+ str(self.isRecording))
        timeDiff = (datetime.now() - self.startTime).seconds
        if not self.isRecording:
            self.isRecording = True
            self.startTime = datetime.now()
            # fourcc = cv2.VideoWriter_fourcc(*'XVID')
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            self.tempVideo = TempFile(basePath="/home/zebra/PythonHome/DetectRecordSend", ext=".mp4")
            self.writer = cv2.VideoWriter(self.tempVideo.path, fourcc, 30, (W, H),True)
            print("Start recording, now = " + str(self.startTime))
            self.fservice.uploadEvent("Attention! Detected Human inside the truck", "warning")
        elif self.isRecording and timeDiff < 10:
            #print("Video record in progress frame "+ str(frame))
            self.writer.write(frame)
        elif self.isRecording:
            self.isRecording = False
            self.writer.write(frame)
            self.writer.release()
            self.writer = None
            print("Time out, stop recording, upload and send sms")
            downloadPath = self.cloud.upload(self.tempVideo)
            # self.cloud.sendSms(downloadPath)
            
        

        

# function to handle keyboard interrupt
def signal_handler(sig, frame):
    # delete the temporary file
    # tempVideo.cleanup()
    print("[INFO] You pressed `ctrl + c`! Closing human detect service!" \
        " application...")
    sys.exit(0)