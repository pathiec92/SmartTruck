import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase import firebase
import os
import threading
import time
import uuid
from report import *
from datetime import datetime


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="MyCloudStorage-3e526dc49133.json"
firebase = firebase.FirebaseApplication('https://mycloudstorage-1135.appspot.com')


class FireReportService:
    def __init__(self, start, end):
        self.shouldRunService = False
        firebase_admin.initialize_app()
        self.db = firestore.client()
        self.truckDic = {}
        self. localLoadIdDic = {}
        self.start = start
        self.end = end
        self.loadBusy = False
        self.leBusy = False
        self.isDone:bool = False
        self.isLoadEventsPulled:bool = False
        self.isVideoEventsPulled:bool = False

        print(u'FireReportService created')
    
    def subscribeTruckId(self):
        print(u'Subscribing for subscribeTruckId')
        doc_ref = self.db.collection('Truck')
        #doc_ref = self.db.collection('Load')
        # Watch the document
        return doc_ref.on_snapshot(self.getTruckIds)
        #return doc_ref.on_snapshot(self.getLoadIds)

    def isOpDone(self):
        return self.isDone

    def isRecordPulled(self):
        return self.isLoadEventsPulled and self.isVideoEventsPulled 

    def getTruckIds(self, doc_snapshot, changes, read_time):
         #print(u'received command document {0}'.format(doc_snapshot))
        c = 0
        prosCount = 0
        for doc in doc_snapshot:
        #    if c > 2: 
        #        break
        #    c+=1
           
           truckId = doc.to_dict().get("truckId")
           sl = doc.to_dict().get("sl")

           self.truckDic[truckId] = Truck(truckId)

           print(u'{}:device truckId, sl = {}, {}'.format(datetime.now(),truckId,sl))
        #    if truckId == 'HT2020100005': 
        #        continue
           #self.subscribe(truckId)
           self.loadBusy = True
           self.launchProcess(truckId)
        #    c = 100
        #     #and self.loadBusy is True
        #    if prosCount != 5:
        #         prosCount += 1
        #         while c > 0 :
        #             time.sleep(0.25)
        #             c -= 1
        #    if prosCount ==5:
        #        prosCount = 0
           print(u'{}: truckId:{}, busy:{}, c:{}, prosCount:{}'.format(datetime.now(),truckId, self.loadBusy, c, prosCount))
        self.isDone = True
        
    def launchProcess(self, truckId):
        print('Starting new process for truck:{}'.format(truckId))
        cm = u'cd ~/SmartTruck/client-raspberry; python3 report_pull_for_id.py -id {} -s {} -e {}'.format(truckId,str(int(self.start)),str(int(self.end)))
        print(u'Command : {}'.format(cm))
        os.system(cm)

    def subscribe(self, truckId):
        truckId = truckId.strip()
        print(u'Subcribe truckId = {}, self.start:{},self.end:{}'.format(truckId,self.start,self.end))
        self.isLoadEventsPulled = False
        self.isVideoEventsPulled = False
        doc_ref = self.db.collection('Load').where(u'truckId',u'==', truckId)
        return doc_ref.on_snapshot(self.getLoadIds)

    def getLoadIds(self, doc_snapshot, changes, read_time):
        c = 0
        print(u'getLoadIds')
        for doc in doc_snapshot:
        #    if c > 2: 
        #        break
        #    c+=1
           dic = doc.to_dict()
           truckId = dic.get("truckId")
           print('truckId before create:{}'.format(truckId))
           if truckId not in self.truckDic:
                print('create new truck:{}'.format(truckId))
                self.truckDic[truckId] = Truck(truckId)
            
           sl = dic.get("sl")
           loadId = doc.id
           self.localLoadIdDic[loadId] = Load(loadId)
           self.truckDic[truckId].loadIdDic[loadId] = Load(loadId=loadId)

           print(u'[getLoadIds] truckId, sl, loadId = {}, {}, {}'.format(truckId,sl,loadId))           
           self.subLoadVideo(truckId, sl, loadId)

        self.loadBusy = False

    def subLoadVideo(self,truckId, sl, loadId):
        
        self.subscribeVideoLink(truckId,sl,loadId)
        self.leBusy = True
        c = 200
        # while c > 0 and self.leBusy is True:
        #     time.sleep(0.25)
        #     c -= 1
        print(u'{}: VideoEvent truckId:{}, loadId:{}, busy:{}, c:{}'.format(datetime.now(),truckId, loadId, self.leBusy, c))

        self.leBusy = False

        self.subscribeLoad(truckId,sl,loadId)
        self.leBusy = True
        c = 200
        # while c > 0 and self.leBusy is True:
        #     time.sleep(0.25)
        #     c -= 1
        print(u'{}: LoadEvent truckId:{}, loadId:{}, busy:{}, c:{}'.format(datetime.now(),truckId, loadId, self.leBusy, c))
        
        self.leBusy = False
        self.isVideoEventsPulled = True


    def subscribeLoad(self, truckId,sl,loadId):
        print(u'*** subscribeLoad truckId={}, loadId={}'.format(truckId, loadId))
        doc_ref = self.db.collection('LoadEvents').document(loadId).collection(loadId)
        return doc_ref.on_snapshot(self.getLoadEvents)

    def getLoadEvents(self, doc_snapshot, changes, read_time):
        
        c = 0
        print(u'getLoadEvents')
        
        for doc in doc_snapshot:
        #    if c > 2: 
        #        break
        #    c+=1
           at = doc.to_dict().get("at")
           msg = doc.to_dict().get("message")
           type = doc.to_dict().get("type")
           loadId = doc.to_dict().get("loadId")
           if loadId in self.localLoadIdDic:
                #print(u'le start:{}, end:{}, at:{}, is:{}'.format(self.convertToStr(self.start), self.convertToStr(self.end), self.convertToStr(at), at > self.start and at < self.end))

                if at > self.start and at < self.end:
                    lt = (at,u'{},{}'.format(type, msg))
                    self.localLoadIdDic[loadId].loadEvent.append(lt)
                    print(u'[getLoadEvents] loadId, type, msg = {}, {}, {}'.format(loadId, type, msg))
        self.leBusy = False
        self.isLoadEventsPulled = False

    def subscribeVideoLink(self, truckId,sl,loadId):
        print(u'*** subscribeVideoLink truckId={}, loadId={}'.format(truckId, loadId))
        doc_ref = self.db.collection('VideoLink').where(u'truckId',u'==', truckId)
        return doc_ref.on_snapshot(self.getVideoLinks)

    def getVideoLinks(self, doc_snapshot, changes, read_time):
        
        c = 0
        print(u'getVideoLinks')
        for doc in doc_snapshot:
        #    if c > 2: 
        #        break
        #    c+=1
           at = doc.to_dict().get("at")
           truckId = doc.to_dict().get("truckId")
           vLink = doc.to_dict().get("vlink")
           loadId = doc.to_dict().get("loadId")
           if loadId in self.localLoadIdDic:
                #print(u'le start:{}, end:{}, at:{}, is:{}'.format(self.convertToStr(self.start), self.convertToStr(self.end), self.convertToStr(at), at > self.start and at < self.end))
                if at > self.start and at < self.end:
                        #lt = (at,vLink.strip())
                        print(u'[getVideoLinks] loadId, truckId, vLink = {}, {}, {}'.format(loadId, truckId, vLink))
                        self.localLoadIdDic[loadId].videoEvent.add(vLink.strip())

        self.leBusy = False

    def stichReportNPrint(self):
        for truckId in self.truckDic:
            truck = self.truckDic[truckId]
            
            for loadId in truck.loadIdDic:
                localLoad = self.localLoadIdDic[loadId]
                truck.loadIdDic[loadId] = localLoad
                print(u'stichReportNPrint, videoEvent len = {}'.format(len(localLoad.videoEvent)))
                print(u'stichReportNPrint, loadEvent len = {}'.format(len(localLoad.loadEvent)))

                

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
        date = datetime.fromtimestamp(self.start/1000.0)
        date = date.strftime('%Y-%m-%d')
        main = u'{}_cambot_reports'.format(date)
        for truckId in self.truckDic:
            truck = self.truckDic[truckId]
            #self.createDir(main+'/'+truckId)
            print(u'--> Truck :{}'.format(truckId))

            for loadId in truck.loadIdDic:
                load = truck.loadIdDic[loadId]
                #self.createDir(main+'/'+truckId +'/'+ loadId)
                print(u'----> Load :{}'.format(loadId))

                print(u'<---- Load Events ---->')
                loadEventsPath = main+'/'+truckId +'/'+ loadId +'/loadEvents.txt'
                if len(load.loadEvent) == 0:
                    print('-No records for {}'.format(loadEventsPath))
                    continue
                self.createDir(main+'/'+truckId +'/'+ loadId)
                f= open(loadEventsPath,'w')
                print(u'loadEvent len = {}'.format(len(load.loadEvent)))
                for l in load.loadEvent:
                    at = l[0]
                    print(u'------> le :{}'.format(l[1]))                    
                    f.write(l[1])
                    f.write('\n')
                f.close()


                print(u'<---- Video Events ---->')
                videoLinksPath = main+'/'+truckId +'/'+ loadId +'/videoLinks.txt'
                if len(load.videoEvent) == 0:
                    print('-No records for {}'.format(loadEventsPath))
                    continue
                self.createDir(main+'/'+truckId +'/'+ loadId)
                f= open(videoLinksPath,'w')
                print(u'videoEvent len = {}'.format(len(load.videoEvent)))
                for l in load.videoEvent:
                    # at = l[0]
                    # print(u'le start:{}, end:{}, at:{}'.format(self.start, self.end, at))
                    print(u'------> ve :{}'.format(l))
                    f.write(l.strip())
                    f.write('\n')
                f.close()

    def createDir(self, folderName):
        path = ""
        current_directory = os.getcwd()
        path = os.path.join(current_directory, folderName)
        if not os.path.exists(path):
            os.makedirs(path)
        return path
    def convertToStr(self,t):
        date = datetime.fromtimestamp(t/1000.0)
        return date.strftime('%Y-%m-%d %H:%M:%S')