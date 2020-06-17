from offline import *
import time
from util import video

# for i in 1,2,3,4,5,6 :
#     now = int(round(time.time() * 1000))
#     loadEvent = {
#             u'loadId' : "currentLoad.loadId"+str(i),
#             u'type': "type"+str(i),
#             u'message': "msg",
#             u'at': now
#         }
#     saveEvent("LoadEvents",loadEvent,None)
#     v = video("loadId_"+str(i),"tid","someLink",i*10)
#     saveEvent("VideoLink",v.getEvent(),None)

uploadOfflineEvents(None)

