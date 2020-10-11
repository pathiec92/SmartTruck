import sys

import time

# function to handle keyboard interrupt
def signal_handler(sig, frame):
    # delete the temporary file
	# tempVideo.cleanup()
	print("[INFO] You pressed `ctrl + c`! Closing mail detector" \
		" application...")
	sys.exit(0)

def fibo(n):
    return n * 4



class Truck:
    def __init__(self,truckId="",owner=""):
        self.truckId = truckId
        self.owner = owner
class Load:
    def __init__(self,loadId,truck):
        self.loadId = loadId
        self.truck = truck


class video:
    def __init__(self,loadId, truckId, vlink, slot):
        self.loadId=loadId
        self.truckId=truckId
        self.vlink=vlink
        self.slot=slot

    def getEvent(self):
        now = int(round(time.time() * 1000))
        videoEvent = {
            u'loadId': self.loadId,
            u'truckId': self.truckId,
            u'vlink': self.vlink,
            u'slot': self.slot,
            u'at': now
        }
        print("video = {}".format(videoEvent))
        return videoEvent

# Singleton objects
currentTruck = Truck()
currentLoad = Load(loadId="",truck=currentTruck)
currentSlot = 20


def getserial():
  # Extract serial from cpuinfo file
    cpuserial = "unknown"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "unknown"
    if len(cpuserial) ==0 or cpuserial == "" or not cpuserial:
        cpuserial = "unknown"
    return cpuserial
