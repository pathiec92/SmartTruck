import sys
import cv2
from imutils.io import TempFile

from datetime import datetime
# initialize the flags for fridge open and notification sent
class state:
    def __init__(self):
        self.isRecording = False
        self.isNotificationSent = False
        self.isPrevRecording = False
        self.startTime = datetime.now()
        self.writer = None
        # self.W = None
        # self.H = None
        self.tempVideo = None

    def recordIt(self,frame, conf):
        (H, W) = frame.shape[:2]
        print("isRecording = "+ str(self.isRecording))
        timeDiff = (datetime.now() - self.startTime).seconds
        if not self.isRecording:
            self.isRecording = True
            self.startTime = datetime.now()
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.tempVideo = TempFile(basePath="/home/zebra/PythonHome/DetectRecordSend", ext=".avi")
            self.writer = cv2.VideoWriter(tempVideo.path, fourcc, 30, (W, H),True)
            print("Start recording, now = " + str(self.startTime))
        elif self.isRecording and timeDiff < 10:
            print("Video record in progress frame "+ str(frame))
            self.writer.write(frame)
        elif self.isRecording:
            self.isRecording = False
            self.writer.write(frame)
            self.writer.release()
            self.writer = None
            print("Time out, stop recording")
        

        

# function to handle keyboard interrupt
def signal_handler(sig, frame):
    # delete the temporary file
    # tempVideo.cleanup()
    print("[INFO] You pressed `ctrl + c`! Closing human detect service!" \
        " application...")
    sys.exit(0)