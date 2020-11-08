from imutils.video import VideoStream
from imutils.video import FPS
from multiprocessing import Process
from multiprocessing import Queue
from pyimagesearch.utils import Conf
from datetime import datetime
import numpy as np
import argparse
import imutils
import time
import cv2

from firestore_service import *
from session import *
from util import *
#from util import signal_handler
import signal
from log import *


def detectHumanAndMove(vf, conf, root):
    dest = '{}/human'.format(root)
    print("[INFO] opening video file..." + f)
    vs = cv2.VideoCapture(vf)
    #vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)
    fps = FPS().start()

    starting_time = time.time()
    identifyhumanCounter = 1

    while True:
        try:
            humandetect = False
            # grab a frame from the video stream
            fullFrame = vs.read()

            # if no frame was read, the stream has ended
            if fullFrame is None:
                break

            # handle the frame whether the frame was read from a VideoCapture
            # or VideoStream
            fullFrame = fullFrame[1]

            # resize the frame apply the background subtractor to generate
            # motion mask

            frame = imutils.resize(fullFrame, width=500)

            cv2.imshow("Frame", frame)

            # grab the frame dimensions and convert it to a blob for Human Detection
            (h, w) = frame.shape[:2]

            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                         0.007843, (300, 300), 127.5)

            # pass the blob through the network and obtain the detections and
            # predictions
            net.setInput(blob)
            detections = net.forward()

            # check to see if our detectios are not None (and if so, we'll
            # draw the detections on the frame)
            if identifyhumanCounter >= 3:
                # loop over the detections
                for i in np.arange(0, detections.shape[2]):
                    # extract the confidence (i.e., probability) associated
                    # with the prediction
                    confidence = detections[0, 0, i, 2]

                    # filter out weak detections by ensuring the `confidence`
                    # is greater than the minimum confidence
                    if confidence < conf["confidence"]:
                        continue

                    # otherwise, extract the index of the class label from
                    # the `detections`, then compute the (x, y)-coordinates
                    # of the bounding box for the object
                    idx = int(detections[0, 0, i, 1])
                    dims = np.array([w, h, w, h])
                    box = detections[0, 0, i, 3:7] * dims
                    (startX, startY, endX, endY) = box.astype("int")
                    if idx == 15:
                        humandetect = True
                if humandetect:
                    print(" Frame Detected Human Detected, vid path: " + vf)
                    moveVideo(vf, dest)
                    break
                identifyhumanCounter = 0
            else:
                identifyhumanCounter += 1
                # show the output frame
            key = cv2.waitKey(1) & 0xFF
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
            # update the FPS counter
            fps.update()
        except:
            print('Exception while anlysing the frame')
            break

        # stop the timer and display FPS information
    fps.stop()
    logger.info(u"[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    logger.info(u"[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    # do a bit of cleanup
    cv2.destroyAllWindows()


logger.info(u'[INFO] loading model...')
print("logger {}", logger)
net = cv2.dnn.readNetFromCaffe(
    "MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")

detections = None

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
                help="Path to the input configuration file")

ap.add_argument("-f", "--folder", required=True,
                help="Specify the root folder")

videosFolder = ""

args = vars(ap.parse_args())
logger.info(u"Args1 are {}".format(args))

# load the configuration file and initialize the Twilio notifier
conf = Conf(args["conf"])
confidenceThreshold = conf["confidence"]
destFolder = args["folder"]

# signal trap to handle keyboard interrupt
signal.signal(signal.SIGINT, signal_handler)
logger.info(u"[INFO] Press `ctrl + c` to exit, or 'q' to quit if you have"
            " the display option on...")

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
for root, subFolders, files in os.walk(os.getcwd()+'/'+destFolder):
    videosFolder = ''
    if os.path.isdir(root) is True:
        #print('--root :{}, subFolders: {}, files: {}'.format(root,subFolders,files))
        vid = os.path.basename(root)
        if vid == 'videos' and os.path.isdir(root):
            print('is vid path:' + vid)
            #print(u'directory {}'.format(root))
            for f in files:
                vf = root+'/'+f
                print('video :' + vf)
                detectHumanAndMove(vf, conf, root)
