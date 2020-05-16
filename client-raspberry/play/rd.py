
from datetime import datetime
# initialize the flags for fridge open and notification sent

class state
isRecording = False
isNotificationSent = False
isPrevRecording = False
startTime = datetime.now()

def recordIt(frame, conf):
    print(conf)
    timeDiff = (datetime.now() - startTime).seconds
    if isRecording and timeDiff < 10:
        print("Video record in progress frame "+ str(frame))
    elif isRecording:
        isRecording = False
        print("Time out, stop recording")
    elif not isRecording:
        isRecording = True
        startTime = datetime.now()
        print("Start recording, now = " + str(startTime))
        


