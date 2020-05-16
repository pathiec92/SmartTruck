import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


from firebase import firebase
import os
import threading
import time
import uuid 


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="MyCloudStorage-3e526dc49133.json"
firebase = firebase.FirebaseApplication('https://mycloudstorage-1135.appspot.com')

class FireStoreService:
    def __init__(self):
        self.shouldRunService = False
        firebase_admin.initialize_app()
        self.db = firestore.client()
        self.currentLoadId = ""
        self.activeload_ref = self.db.collection(u'ActiveLoad')

    def subScribeActiveLoad(self):
        doc_ref = self.db.collection(u'ActiveLoad')
        # Watch the document
        return doc_ref.on_snapshot(self.on_snapshot)
       

    def on_snapshot(self, doc_snapshot, changes, read_time):
        doc_ref = self.db.collection(u'ActiveLoad')
        if len(doc_snapshot)== 0 :
            print('STOP FRAUD DETECTION SERVICE')
            self.shouldRunService = False
            self.uploadLoadEvent("Stopped fraud detection service at truck.")
            return
        
        for doc in doc_snapshot:
            print(u'Received document snapshot: {} => {}'.format(doc.id, doc.to_dict()))
            loadId = doc.to_dict().get("loadId")
            truckAck = doc.to_dict().get("truckAck")
            self.currentLoadId = loadId
            if truckAck is None:
                data = {
                    u'truckAck' : {
                        u'loadId': loadId,
                        u'truckNum': "KA03 HM4737",
                        u'ownerName': "Pampi"
                    }
                }
                print('START FRAUD DETECTION SERVICE')
                doc_ref.document(loadId).update(data)
                self.uploadLoadEvent("Started Fraud detection service at truck")
            self.shouldRunService = True            
            break

    def uploadLoadEvent(self, msg):
       self.uploadEvent(msg,"dark")
        
    def uploadEvent(self,msg, t):
        if self.currentLoadId == "" : 
            print("currentLoadId is empty")
            return
        now = int(round(time.time() * 1000))
        loadEvent = {
            u'type': t,
            u'message': msg,
            u'at': now
        }
        uid = str(uuid.uuid4())
        loadevent_ref = self.db.collection(u'LoadEvents').document(self.currentLoadId).collection(self.currentLoadId).document(uid).set(loadEvent)
    



 
    

