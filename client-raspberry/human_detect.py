from imutils.video import VideoStream
from imutils.video import FPS
from pyimagesearch.utils import Conf
from datetime import datetime
import numpy as np
import argparse
import imutils
import time
import cv2

from firestore_service import *
from session import *
from util import currentTruck
from util import signal_handler
import signal
from log import *

#Load YOLO
#net = cv2.dnn.readNet("yolov3.weights","yolov3.cfg") # Original yolov3
#net = cv2.dnn.readNet("yolov3-tiny.weights","yolov3-tiny.cfg") #Tiny Yolo
# load our serialized model from disk
logger.info(u'[INFO] loading model...')
print("logger {}", logger)
net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")
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
ap.add_argument("-dv", "--delv",  action="store_true",
	help="Delete Video cache (Y/N)")
args = vars(ap.parse_args())
logger.info(u"Args1 are {}".format(args))

# load the configuration file and initialize the Twilio notifier
conf = Conf(args["conf"])
truckId = conf["truckId"]
currentTruck.truckId = truckId
currentTruck.owner = conf["owner"]
confidenceThreshold = conf["confidence"]

#subscribe for ActiveLoad
fireStoreService = FireStoreService(truckId)

wait_sub = fireStoreService.subScribeActiveLoad()

#s = state(conf, fireStoreService)
def onSessionComplete():
    logger.info(u"Session completed!!")

ses = session(onSessionComplete, fireStoreService)

# signal trap to handle keyboard interrupt
signal.signal(signal.SIGINT, signal_handler)
logger.info(u"[INFO] Press `ctrl + c` to exit, or 'q' to quit if you have" \
	" the display option on...")

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
logger.info(u"[INFO] starting video stream...")
vs = VideoStream(0).start()
time.sleep(2.0)
fps = FPS().start()

# font = cv2.FONT_HERSHEY_PLAIN
starting_time= time.time()
frame_id = 0
motionCounter = 0
avg = None



while True:
    #logger.info(str(fireStoreService.shouldRunService))
    if fireStoreService.shouldRunService is False :
        time.sleep(1)
        continue
    time.sleep(0.25)

     # grab the current frame and initialize the occupied/unoccupied
	# text
    frame = vs.read()
    envichange = False
    peopledetect = False
    motiondetect = False
    timestamp = datetime.now()
    text = "Environment Not Changed..."

    # if the frame could not be grabbed, then we have reached the end
	# of the video
    if frame is None:
        break
   
    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=300)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the average frame is None, initialize it
    if avg is None:
        logger.info(u"[INFO] starting background model...")
        avg = gray.copy().astype("float")
        #rawCapture.truncate(0)
        continue

    # accumulate the weighted average between the current frame and
	# previous frames, then compute the difference between the current
	# frame and running average
    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

    # threshold the delta image, dilate the thresholded image to fill
	# in holes, then find contours on thresholded image
    thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
        cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < conf["min_area"]:
            continue
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        envichange = True
        text = "Environment Changed..."

    
    # draw the text and timestamp on the frame
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, "Vehicle Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
        0.35, (0, 0, 255), 1)

    # check to see if the room is occupied
    if envichange:
        # increment the motion counter
        motionCounter += 1
        #logger.info(motionCounter)
        # check to see if the number of frames with consistent motion is
        # high enough
        if motionCounter >= conf["min_motion_frames"]:
            # check to see if dropbox sohuld be used
            motiondetect = True
            motionCounter = 0

            # grab the frame dimensions and convert it to a blob
            height,width,channels = frame.shape
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)    

            # pass the blob through the network and obtain the detections and
            # predictions
            net.setInput(blob)
            detections = net.forward()

            # loop over the detections
            for i in np.arange(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with
                # the prediction
                confidence = detections[0, 0, i, 2]
                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence > confidenceThreshold:
                    # extract the index of the class label from the
                    # `detections`, then compute the (x, y)-coordinates of
                    # the bounding box for the object
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                    (startX, startY, endX, endY) = box.astype("int")
                    # draw the prediction on the frame
                    label = "{}: {:.2f}%".format(CLASSES[idx],
                        confidence * 100)
                    cv2.rectangle(frame, (startX, startY), (endX, endY),
                        COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(frame, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                    peopledetect = True
    # otherwise, the room is not occupied
    else:
        motionCounter = 0
    if motiondetect:
        logger.info(u"Truck Inside Staus: Enviornmen Changed at {}".format(datetime.now()))
        ses.humanDetected(frame)
        if peopledetect:
            logger.info(u"[Message] Truck Inside Staus: Human Detected at {}".format(datetime.now()))
            ses.isSendMessage = True
    else :
        ses.captureFrames(frame)
            
        
# show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
	# update the FPS counter
    fps.update()

    # stop the timer and display FPS information
fps.stop()
logger.info(u"[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
logger.info(u"[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()    

