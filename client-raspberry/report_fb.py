import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase import firebase
import os
import threading
import time
import uuid
from report import *



os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="MyCloudStorage-3e526dc49133.json"
firebase = firebase.FirebaseApplication('https://mycloudstorage-1135.appspot.com')


class FireReportService:
    def __init__(self,truckId = ""):
        self.shouldRunService = False
        firebase_admin.initialize_app()
        self.db = firestore.client()
        self.truckDic = {}
        self. localLoadIdDic = {}
        print(u'FireReportService created')
    
    def subscribeTruckId(self):
        print(u'Subscribing for subscribeTruckId')
        doc_ref = self.db.collection('Truck')
        # Watch the document
        return doc_ref.on_snapshot(self.getTruckIds)

    def getTruckIds(self, doc_snapshot, changes, read_time):
         #print(u'received command document {0}'.format(doc_snapshot))
        c = 0
        for doc in doc_snapshot:
           if c > 2: 
               break
           c+=1
           
           truckId = doc.to_dict().get("truckId")
           sl = doc.to_dict().get("sl")

           self.truckDic[truckId] = Truck(truckId)

           print(u'device truckId, sl = {}, {}'.format(truckId,sl))
           self.subscribe(truckId)

    def subscribe(self, truckId):
        print(u'Subcribe truckId = {}'.format(truckId))
        doc_ref = self.db.collection('Load').where(u'truckId',u'==', truckId)
        return doc_ref.on_snapshot(self.getLoadIds)

    def getLoadIds(self, doc_snapshot, changes, read_time):
        c = 0
        print(u'getLoadIds')
        for doc in doc_snapshot:
           if c > 2: 
               break
           c+=1
           truckId = doc.to_dict().get("truckId")
           sl = doc.to_dict().get("sl")
           loadId = doc.to_dict().get("id")
           self.localLoadIdDic[loadId] = Load(loadId=loadId)
           self.truckDic[truckId].loadIdDic[loadId] = Load(loadId=loadId)

           print(u'[getLoadIds] truckId, sl, loadId = {}, {}, {}'.format(truckId,sl,loadId))
           self.subscribeVideoLink(truckId,sl,loadId)
           self.subscribeLoad(truckId,sl,loadId)

    def subscribeLoad(self, truckId,sl,loadId):
        print(u'*** subscribeLoad truckId={}'.format(truckId))
        doc_ref = self.db.collection('LoadEvents').document(loadId).collection(loadId)
        return doc_ref.on_snapshot(self.getLoadEvents)

    def getLoadEvents(self, doc_snapshot, changes, read_time):
        c = 0
        print(u'getLoadEvents')
        
        for doc in doc_snapshot:
           if c > 2: 
               break
           c+=1
           msg = doc.to_dict().get("message")
           type = doc.to_dict().get("type")
           loadId = doc.to_dict().get("loadId")
           if loadId in self.localLoadIdDic:
                self.localLoadIdDic[loadId].loadEvent.append(u'{},{}'.format(type, msg))
                print(u'[getLoadEvents] loadId, type, msg = {}, {}, {}'.format(loadId, type, msg))

    def subscribeVideoLink(self, truckId,sl,loadId):
        print(u'*** subscribeLoad truckId={}'.format(truckId))
        doc_ref = self.db.collection('VideoLink').where(u'truckId',u'==', truckId)
        return doc_ref.on_snapshot(self.getVideoLinks)

    def getVideoLinks(self, doc_snapshot, changes, read_time):
        c = 0
        print(u'getVideoLinks')
        for doc in doc_snapshot:
           if c > 2: 
               break
           c+=1
           truckId = doc.to_dict().get("truckId")
           vLink = doc.to_dict().get("vlink")
           loadId = doc.to_dict().get("loadId")
           print(u'[getVideoLinks] loadId, truckId, vLink = {}, {}, {}'.format(loadId, truckId, vLink))
           self.localLoadIdDic[loadId].videoEvent.append(u'{}'.format(vLink))

    def stichReportNPrint(self):
        for truckId in self.truckDic:
            truck = self.truckDic[truckId]
            for loadId in truck.loadIdDic:
                localLoad = self.localLoadIdDic[loadId]
                truck.loadIdDic[loadId] = localLoad
                

    def printReport(self):
        for truckId in self.truckDic:
            truck = self.truckDic[truckId]
            print(u'--> Truck :{}'.format(truckId))

            for loadId in truck.loadIdDic:
                load = truck.loadIdDic[loadId]
                print(u'----> Load :{}'.format(loadId))
                print(u'<---- Load Events ---->')
                for l in load.loadEvent:
                    print(u'------> le :{}'.format(l))
                print(u'<---- Video Events ---->')
                for l in load.loadEvent:
                    print(u'------> ve :{}'.format(l))
    
    def writeReport(self):
        main = 'report'
        for truckId in self.truckDic:
            truck = self.truckDic[truckId]
            self.createDir(main+'/'+truckId)
            print(u'--> Truck :{}'.format(truckId))

            for loadId in truck.loadIdDic:
                load = truck.loadIdDic[loadId]
                self.createDir(main+'/'+truckId +'/'+ loadId)
                print(u'----> Load :{}'.format(loadId))

                print(u'<---- Load Events ---->')
                loadEventsPath = main+'/'+truckId +'/'+ loadId +'/loadEvents.txt'
                #self.createDir(loadEventsPath)
                f= open(loadEventsPath,'w')
                for l in load.loadEvent:
                    print(u'------> le :{}'.format(l))                    
                    f.write(l)
                    f.write('\n')
                f.close()


                print(u'<---- Video Events ---->')
                videoLinksPath = main+'/'+truckId +'/'+ loadId +'/videoLinks.txt'
                #self.createDir(videoLinksPath)
                f= open(videoLinksPath,'w')
                for l in load.videoEvent:
                    print(u'------> ve :{}'.format(l))
                    f.write(l)
                    f.write('\n')
                f.close()

    def createDir(self, folderName):
        path = ""
        current_directory = os.getcwd()
        path = os.path.join(current_directory, folderName)
        if not os.path.exists(path):
            os.makedirs(path)
        return path






    
