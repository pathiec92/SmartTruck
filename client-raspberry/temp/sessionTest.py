from session import *
from slot import *
#import _thread
import threading

def onSessionComplete():
    print("Session completed!!")

ses = session(onSessionComplete)

while(True):
    print("Waiting for input")
    v = int(input())
    print(str(v))
    if v == 0:
        t= threading.Thread(target=ses.startSession,args=())
        t.start()
        print("[Session] Started")
    elif v == 1:
        ses.humanDetected()
    elif v == 2:
        ses.isDetected = False




# def onComplete():
#     print("Slot completed")
# slot = slot(onComplete)
# while(True):
#     print("Waiting for input")
#     v = int(input())
#     print(str(v))
#     if v == 0:
#         t= threading.Thread(target=slot.startSlot,args=(5,))
#         t.start()
#         print("[Session] Started the slot")
#     elif v == 1:
#         slot.isStopSlot = True
#     elif v == 2:
#         slot.isStopSlot = False