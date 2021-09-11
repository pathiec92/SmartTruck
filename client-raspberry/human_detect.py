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
from util import currentTruck
from util import signal_handler
import signal
from log import *

from critical import *

def classify_frame(net, inputQueue, outputQueue):
	# keep looping
	while True:
		# check to see if there is a frame in our input queue
		if not inputQueue.empty():
			# grab the frame from the input queue, resize it, and
			# construct a blob from it
			frame = inputQueue.get()
			frame = cv2.resize(frame, (300, 300))
			blob = cv2.dnn.blobFromImage(frame, 0.007843,
				(300, 300), 127.5)

			# set the blob as input to our deep learning object
			# detector and obtain the detections
			net.setInput(blob)
			detections = net.forward()

			# write the detections to the output queue
			outputQueue.put(detections)

logger.info(u'[INFO] loading model...')
print("logger {}", logger)
net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")

# initialize the input queue (frames), output queue (detections),
# and the list of actual detections returned by the child process
inputQueue = Queue(maxsize=1)
outputQueue = Queue(maxsize=1)
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
automeanCal = conf["automeanCal"]
truckenvithresh = conf ["truckenvithresh"]
camSource = conf["camSource"]
camRotate180 = conf["camRotate180"]
camRotate90 = conf["camRotate90"]
camRotateC90 = conf["camRotateC90"]

#subscribe for ActiveLoad
fireStoreService = FireStoreService()
fireStoreService.instance = 'main'
wait_sub = fireStoreService.subScribeActiveLoad()
#fireStoreService.subscribeCommand()

critical = Critical(fireStoreService)
#s = state(conf, fireStoreService)
def onSessionComplete():
    logger.info(u"Session completed!!")

ses = session(onSessionComplete, fireStoreService)

# signal trap to handle keyboard interrupt
signal.signal(signal.SIGINT, signal_handler)
logger.info(u"[INFO] Press `ctrl + c` to exit, or 'q' to quit if you have" \
	" the display option on...")

# construct a child process *indepedent* from our main process of
# execution
print("[INFO] starting process...")
p = Process(target=classify_frame, args=(net, inputQueue,
	outputQueue,))
p.daemon = True
p.start()

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
logger.info(u"[INFO] starting video stream...")
if camSource == "USBCamera":
	vs = VideoStream(src=0).start()
	#vs = VideoStream(-1).start()
elif camSource == "PiCamera":
	vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

fps = FPS().start()

starting_time= time.time()

enviprofileSet = False

enviprofileCounter = 1
truckmaxthreshmean = 0
avg = None
avgmean=0
dooropenCounter = 1
doorclosedCounter =1
truckdoorClose=False
truckdoorOpen = False

while True:
	#motionDetect = False
	humandetect = False
	text = "Unoccupied"
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
	
	if camRotate180:
		frame = cv2.rotate(frame, cv2.ROTATE_180)
	elif camRotate90:
		frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
	elif camRotateC90:
		frame = cv2.rotate(frame,cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)

	# Pre Process the Frame 
	frame_original = imutils.resize(frame, width=400)

	# draw the text and timestamp on the frame
	ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	# cv2.putText(frame_original, ts, (10, frame_original.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
	#                0.35, (0, 0, 255), 1)

	ses.captureFrames(frame_original)
	
	gray = cv2.cvtColor(frame_original,cv2.COLOR_BGR2GRAY)
	
	# The declaration of CLAHE  
	# clipLimit -> Threshold for contrast limiting 
	#clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(5,5)) 
	#gray = clahe.apply(gray) + 30

	fame_processed = np.zeros_like(frame_original)
	fame_processed[:,:,0] = gray
	fame_processed[:,:,1] = gray
	fame_processed[:,:,2] = gray

	# grab the frame dimensions and convert it to a blob for Human Detection
	(h, w) = fame_processed.shape[:2]
	#(h, w) = frame_original.shape[:2]

	# if the input queue *is* empty, give the current frame to
	# classify
	if inputQueue.empty():
		inputQueue.put(fame_processed)
		#inputQueue.put(frame_original)

	# if the output queue *is not* empty, grab the detections
	if not outputQueue.empty():
		detections = outputQueue.get()


	# blob = cv2.dnn.blobFromImage(cv2.resize(fame_processed, (300, 300)),
	#    0.007843, (300, 300), 127.5)

	# pass the blob through the network and obtain the detections and
	# predictions
	# net.setInput(blob)
	# detections = net.forward()

	# check to see if our detectios are not None (and if so, we'll
	# draw the detections on the frame)
	if detections is not None:
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
				# draw the prediction on the frame
				label = "{}: {:.2f}%".format(CLASSES[idx],confidence * 100)
				cv2.rectangle(frame_original, (startX, startY), (endX, endY),
				COLORS[idx], 2)
				y = startY - 15 if startY - 15 > 15 else startY + 15
				cv2.putText(frame_original, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
				cv2.putText(frame_original, "Truck Status: {}".format("Human Detected"), (10, 20),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
				
	if humandetect:
		if dooropenCounter >= conf["min_dooropen_frames"]:
			logger.info(u"Truck Status: Door Opened (Human Detected...) at {}".format(datetime.now()))
			print("Truck Inside Status: Door Opened (Human Detected...) at ", datetime.now())
			ses.humanDetected(frame_original)
			ses.isSendMessage = True
			dooropenCounter = 0
		else:
			dooropenCounter += 1
	else:
		if doorclosedCounter >= conf["min_doorclosed_frames"]:
			#logger.info(u"Truck Status: Door Closed at {}".format(datetime.now()))
			#print("Truck Status: Door Closed at ", datetime.now()) 		
			doorclosedCounter = 0
		else:
			doorclosedCounter += 1	
		
	# show the output frame
	#cv2.imshow("Frame", frame_original)
	#cv2.imshow("Frame", frame_original)
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
print ("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()    

