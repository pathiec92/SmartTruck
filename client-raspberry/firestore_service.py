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


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="MyCloudStorage-3e526dc49133.json"
firebase = firebase.FirebaseApplication('https://mycloudstorage-1135.appspot.com')

class FireStoreService:
    def __init__(self,truckId):
        self.shouldRunService = False
        firebase_admin.initialize_app()
        self.db = firestore.client()
        self.truckId = truckId
        #self.activeload_ref = self.db.collection(u'ActiveLoad')

    def subScribeActiveLoad(self):
        doc_ref = self.db.collection(u'ActiveLoad')
        # Watch the document
        return doc_ref.on_snapshot(self.on_snapshot)
    

    def on_snapshot(self, doc_snapshot, changes, read_time):
        doc_ref = self.db.collection(u'ActiveLoad')
        if len(doc_snapshot)== 0 :
            self.stopService()
            return
        isActiveLoadAvail = False
        for doc in doc_snapshot:
            print(u'Received document snapshot: {} => {}'.format(doc.id, doc.to_dict()))
            truckId = doc.to_dict().get("truckId")
            print(u'self.truckId = {}, fb.truckId = {}'.format(self.truckId, truckId))
            if self.truckId == truckId :
                isActiveLoadAvail = True
                print(u'found my truck {}'.format(truckId))
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
                    print('START FRAUD DETECTION SERVICE')
                    doc_ref.document(loadId).update(data)
                    self.uploadLoadEvent("Started Fraud detection service at truck")
                self.shouldRunService = True            
                break
        if isActiveLoadAvail is False:
            self.stopService()


    def stopService(self):
        print('STOP FRAUD DETECTION SERVICE')
        self.shouldRunService = False
        self.uploadLoadEvent("Stopped fraud detection service at truck.")

    def uploadLoadEvent(self, msg):
       self.uploadEvent(msg,"dark")
    
    def uploadEvent(self,msg, t):
        if currentLoad.loadId == "" : 
            print("currentLoadId is empty")
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
            print("[Offline] device offline, LoadEvents TBD {}".format(loadEvent))
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
            print("[Offline] device offline, VideoLink TBD {}".format(v.getEvent()))

            #saveEvent("VideoLink",v.getEvent,self)
        
    def uploadVLinkDic(self,dic):
        uid = str(uuid.uuid4())
        loadevent_ref = self.db.collection(u'VideoLink').document(uid).set(dic)

    



 
    

