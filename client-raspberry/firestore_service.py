import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase import firebase
import os
import threading
import time
import uuid
from util import video
from util import currentLoad
from util import currentSlot
from offline import *
from log import *
from command_service import *
from configs import *


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="MyCloudStorage-3e526dc49133.json"
firebase = firebase.FirebaseApplication('https://mycloudstorage-1135.appspot.com')

class FireStoreService:
    def __init__(self,truckId = ""):
        self.shouldRunService = False
        firebase_admin.initialize_app()
        self.db = firestore.client()
        self.configs = Configs()
        self.truckId = self.configs.truckId
        self.command = Command(truckId, self, self.configs)
        
        #self.activeload_ref = self.db.collection(u'ActiveLoad')

    def subScribeActiveLoad(self):
        doc_ref = self.db.collection(u'ActiveLoad')
        # Watch the document
        return  doc_ref.on_snapshot(self.on_snapshot)

    def subscribeCommand(self):
        logger.info(u'Subscribing for command')
        print(u'Subscribing for command')
        truckCol = u'Truck/{0}/command'.format(self.truckId)
        print(u'Truck collection = {}'.format(truckCol))
        doc_ref = self.db.collection(truckCol)
        # Watch the document
        return doc_ref.on_snapshot(self.command.serve)
    

    

    def on_snapshot(self, doc_snapshot, changes, read_time):
        doc_ref = self.db.collection(u'ActiveLoad')
        if len(doc_snapshot)== 0 :
            self.stopService()
            return
        isActiveLoadAvail = False
        for doc in doc_snapshot:
            logger.info(u'Received document snapshot: {} => {}'.format(doc.id, doc.to_dict()))
            truckId = doc.to_dict().get("truckId")
            sl = doc.to_dict().get("sl")
            logger.info(u'self.configs.serialNum = {}, fb.sl = {}, {}'.format(self.configs.serialNum, sl, truckId))
            if self.configs.serialNum == sl :
                isActiveLoadAvail = True
                self.configs.serialNum = sl
                self.configs.truckId = truckId
                logger.info(u'found my truck {}'.format(truckId))
                loadId = doc.to_dict().get("loadId")
                truckAck = doc.to_dict().get("truckAck")
                currentLoad.loadId = loadId
                if truckAck is None:
                    data = {
                        u'truckAck' : {
                            u'loadId': loadId,
                            u'truckNum': truckId,
                            u'ownerName': "Pampi"
                        }
                    }
                    logger.info(u'START FRAUD DETECTION SERVICE')
                    doc_ref.document(loadId).update(data)
                    self.uploadLoadEvent("Started Fraud detection service at truck")
                self.shouldRunService = True            
                break
        if isActiveLoadAvail is False:
            self.stopService()


    def stopService(self):
        logger.info(u'STOP FRAUD DETECTION SERVICE')
        self.shouldRunService = False
        self.uploadLoadEvent("Stopped fraud detection service at truck.")

    def uploadLoadEvent(self, msg):
       self.uploadEvent(msg,"dark")
    
    def uploadEvent(self,msg, t):
        if currentLoad.loadId == "" : 
            logger.info(u"currentLoadId is empty")
            return
        now = int(round(time.time() * 1000))
        loadEvent = {
            u'loadId' : currentLoad.loadId,
            u'type': t,
            u'message': msg,
            u'at': now
        }
        if isConnected():
            self.uploadEventDic(loadEvent)
        else :
            logger.info(u"[Offline] device offline, LoadEvents TBD {}".format(loadEvent))
            #saveEvent("LoadEvents", loadEvent,self)
       
    def uploadEventDic(self,dic):
        loadId = dic["loadId"]
        uid = str(uuid.uuid4())
        loadevent_ref = self.db.collection(u'LoadEvents').document(loadId).collection(loadId).document(uid).set(dic)


    def uploadVLink(self,vlink):
        v = video(currentLoad.loadId, currentLoad.truck.truckId, vlink, currentSlot)
        if isConnected():
            self.uploadVLinkDic(v.getEvent())
        else :
            logger.info(u"[Offline] device offline, VideoLink TBD {}".format(v.getEvent()))

            #saveEvent("VideoLink",v.getEvent,self)
        
    def uploadVLinkDic(self,dic):
        uid = str(uuid.uuid4())
        loadevent_ref = self.db.collection(u'VideoLink').document(uid).set(dic)

    def publishDeviceId(self):
        uid = str(uuid.uuid4())
        now = int(round(time.time() * 1000))
        deviceDic = {
            u'sl' : self.configs.serialNum,
            u'at': now
        }
        print(u'deviceDic = {}'.format(deviceDic))
        loadevent_ref = self.db.collection(u'Device').document(self.configs.serialNum).set(deviceDic)

    def updateCommand(self, dic):
        truckId = dic["truckId"]
        loadevent_ref = self.db.collection(u'Truck').document(truckId).collection("command").document("0").set(dic)
        return