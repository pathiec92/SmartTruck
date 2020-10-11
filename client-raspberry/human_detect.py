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
fireStoreService.subscribeCommand()

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

dooropenCounter = 1
truckdoorClose=False
truckdoorOpen = False

while True:
    truckenviBright = False
    truckenviDark = False
    humandetect = False
    truckdoorOpen = False
    truckdoorClose=False
    #logger.info(str(fireStoreService.shouldRunService))
    if fireStoreService.shouldRunService is False :
        time.sleep(1)
        continue
    time.sleep(0.03)

     # grab the current frame and initialize the occupied/unoccupied
	# text
    frame = vs.read()
    
    timestamp = datetime.now()

    # if the frame could not be grabbed, then we have reached the end
	# of the video
    if frame is None:
        break
    
# Pre Process the Frame 
    frame = cv2.rotate(frame, cv2.ROTATE_180)
    cv2.imshow("Frame", frame)
    frame_original = imutils.resize(frame, width=300)
    if(ses.isDetected):
        ses.captureFrames(frame_original)
        continue
    gray = cv2.cvtColor(frame_original,cv2.COLOR_BGR2GRAY)
    
    # The declaration of CLAHE  
	# clipLimit -> Threshold for contrast limiting 
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)) 
    gray = clahe.apply(gray) + 30

    fame_processed = np.zeros_like(frame_original)
    fame_processed[:,:,0] = gray
    fame_processed[:,:,1] = gray
    fame_processed[:,:,2] = gray

    # calculate the average of all pixels where a higher mean
	# indicates that there is more light coming into the truck
    mean = np.mean(gray)
    
    # print (mean)
    # determine if the environment is changed inside truck
    if mean > conf["truckenvithresh"]:
        truckenviBright = True
        # print ("Bright Environment")
    else:
        truckenviDark = True  
        # print ("Dark Environment")  
    if dooropenCounter >= conf["min_dooropen_frames"]:
        if truckenviBright and not truckdoorOpen:
            truckdoorOpen= True
            truckdoorClose = False
            logger.info(u"Truck Inside Status: Door Opened (due to more light coming in...) at {}".format(datetime.now()))
            print("Truck Inside Status: Door Opened (due to more light coming in...) at ", datetime.now()) 
        elif truckenviDark and not truckdoorClose:
            truckdoorClose = True
            truckdoorOpen = False
            logger.info(u"Truck Inside Status: Door Closed (due to low light inside...) at {}".format(datetime.now()))
            print("Truck Inside Status: Door Closed (due to low light inside...) at ", datetime.now()) 
        dooropenCounter = 0
    else:
        dooropenCounter += 1

    # grab the frame dimensions and convert it to a blob for Human Detection
    (h, w) = fame_processed.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(fame_processed, (300, 300)),
        0.007843, (300, 300), 127.5)

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
        if confidence > conf["confidence"]:
            # extract the index of the class label from the
            # `detections`, then compute the (x, y)-coordinates of
            # the bounding box for the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            if idx == 15:
                humandetect = True
                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(CLASSES[idx],
                    confidence * 100)
                cv2.rectangle(frame_original, (startX, startY), (endX, endY),
                    COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame_original, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    if humandetect or truckdoorOpen:
        logger.info(u"Truck Inside Status: Human Detected at {}".format(datetime.now()))
        print("Truck Inside Status: Human Detected at ", datetime.now())
        ses.humanDetected(frame_original)
        ses.isSendMessage = True
        
            
        
# show the output frame
    cv2.imshow("Frame", frame_original)
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

