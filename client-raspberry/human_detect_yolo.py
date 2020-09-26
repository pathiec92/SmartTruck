import cv2
import numpy as np
import time
import signal
#from tools import *
import argparse
from pyimagesearch.utils import Conf
from firestore_service import *
from session import *
from util import currentTruck
from util import signal_handler

#Load YOLO
#net = cv2.dnn.readNet("yolov3.weights","yolov3.cfg") # Original yolov3
#net = cv2.dnn.readNet("yolov3-tiny.weights","yolov3-tiny.cfg") #Tiny Yolo
# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")
classes = []
with open("coco.names","r") as f:
    classes = [line.strip() for line in f.readlines()]

print(classes)

layer_names = net.getLayerNames()
outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

colors= np.random.uniform(0,255,size=(len(classes),3))

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
	help="Path to the input configuration file")
ap.add_argument("-dv", "--delv",  action="store_true",
	help="Delete Video cache (Y/N)")
args = vars(ap.parse_args())
print("Args1 are {}".format(args))

# load the configuration file and initialize the Twilio notifier
conf = Conf(args["conf"])
truckId = conf["truckId"]
currentTruck.truckId = truckId
currentTruck.owner = conf["owner"]

#subscribe for ActiveLoad
fireStoreService = FireStoreService(truckId)

wait_sub = fireStoreService.subScribeActiveLoad()

#s = state(conf, fireStoreService)
def onSessionComplete():
    print("Session completed!!")

ses = session(onSessionComplete, fireStoreService)

# signal trap to handle keyboard interrupt
signal.signal(signal.SIGINT, signal_handler)
print("[INFO] Press `ctrl + c` to exit, or 'q' to quit if you have" \
	" the display option on...")

#loading image
cap=cv2.VideoCapture(0) #0 for 1st webcam
font = cv2.FONT_HERSHEY_PLAIN
starting_time= time.time()
frame_id = 0



while True:
    #print(str(fireStoreService.shouldRunService))
    if fireStoreService.shouldRunService is False :
        time.sleep(1)
        continue

    _,frame= cap.read()
    frame_id+=1
    #cv2.imshow("Image",frame)
    # Our operations on the frame come here
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("Image",frame)
    height,width,channels = frame.shape
    #detecting objects
    blob = cv2.dnn.blobFromImage(frame,0.00392,(320,320),(0,0,0),True,crop=False) #reduce 416 to 320    

    net.setInput(blob)
    outs = net.forward(outputlayers)
    #print(outs[1])


    #Showing info on screen/ get confidence score of algorithm in detecting an object in blob
    class_ids=[]
    confidences=[]
    boxes=[]
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                #onject detected
                center_x= int(detection[0]*width)
                center_y= int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                #cv2.circle(img,(center_x,center_y),10,(0,255,0),2)
                #rectangle co-ordinaters
                x=int(center_x - w/2)
                y=int(center_y - h/2)
                #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

                boxes.append([x,y,w,h]) #put all rectangle areas
                confidences.append(float(confidence)) #how confidence was that object detected and show that percentage
                class_ids.append(class_id) #name of the object tha was detected

    indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.4,0.6)


    for i in range(len(boxes)):
        if i in indexes:
            x,y,w,h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence= confidences[i]
            color = colors[class_ids[i]]
            cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
            cv2.putText(frame,label+" "+str(round(confidence,2)),(x,y+30),font,1,(255,255,255),2)
            #print(label, str(round(confidence,2)))
            ses.humanDetected(frame)
            # if(label == "person"):
            #     print("Detected human trigger video capture")
            #     ses.humanDetected(frame)
            

    elapsed_time = time.time() - starting_time
    fps=frame_id/elapsed_time
    cv2.putText(frame,"FPS:"+str(round(fps,2)),(10,50),font,2,(0,0,0),1)
    
    cv2.imshow("Image",frame)
    key = cv2.waitKey(1) #wait 1ms the loop will start again and we will process the next frame
    
    if key == 27: #esc key stops the process
        break;
    
cap.release()    
cv2.destroyAllWindows()    

