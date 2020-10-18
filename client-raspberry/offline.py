import socket
import os 
import uuid
import json
from glob import glob
from abc import ABC,abstractmethod 
import threading
import time
from util import currentLoad, currentSlot
from imutils.io import TempFile
from log import *

def isConnected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        sock = socket.create_connection(("www.google.com", 80))
        if sock is not None:
            #logger.info(u'Closing socket')
            sock.close
        return True
    except OSError:
        pass
    return False

def createDir(folderName):
    path = ""
    current_directory = os.getcwd()
    path = os.path.join(current_directory, folderName)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def removeDir(folderName):
    path = ""
    current_directory = os.getcwd()
    path = os.path.join(current_directory, folderName)
    if os.path.exists(path):
        logger.info('Removing the files under folder {}'.format(path))
        files  = [f for f in glob(path+'/**', recursive=True) if os.path.isfile(f)]
        for fl in files:
            os.remove(fl)

class OfflineWorker:
    def __init__(self,uploadOffline, notifyOnline):
        self.isOfflineStarted = False
        self.uploadOffline = uploadOffline
        self.notifyOnline = notifyOnline
        if isConnected() is False:
            self.startOnlineIfNot()

    def startOnlineIfNot(self):
        if self.isOfflineStarted is False:
            self.isOfflineStarted = True
            t= threading.Thread(target=self.startOffline,args=())
            t.start()

    def startOffline(self):
        while True:
            time.sleep(2)
            if isConnected():
                logger.info(u"We are back to Online")
                #uploadOfflineEvents(self.fs)
                self.notifyOnline()
                self.uploadOfflineVLink()
                self.isOfflineStarted = False
                break
            logger.info(u"waiting for internet...")


    # def saveEvent(self, event, dic, fs):
    #     path = createDir('.eJson/'+event)+"/"
    #     uid = path+str(uuid.uuid4())+'.json'
    #     with open(uid, 'w') as json_file:
    #         json.dump(dic, json_file)


    def saveVLink(self, path, meta):
        self.startOnlineIfNot()
        dic = {
            u'path':path,
            u'meta':str(meta),
            u'loadId':currentLoad.loadId,
            u'slot': currentSlot
        }
        path = createDir('.vLinks')+"/"
        uid = path+str(uuid.uuid4())+'.json'
        logger.info(u"[Offline] saving vLink {}".format(dic))
        with open(uid, 'w') as json_file:
            json.dump(dic, json_file)

    def uploadOfflineVLink(self):       
        files  = [f for f in glob(os.getcwd()+'/.vLinks/**', recursive=True) if os.path.isfile(f)]
        logger.info(u"[offline] uploading files {}".format(str(files)))
        for fl in files:
            logger.info(u"[Offline] Opening the file {}".format(fl))
            with open(fl) as f:
                dic = json.load(f)
                logger.info(u"[Offline] dic {}".format(dic))
                currentLoad.loadId= dic['loadId']
                currentSlot=dic['slot']
                temp = TempFile()
                temp.path = dic['path']
                t= threading.Thread(target=self.uploadOffline,args=(temp,))
                t.start()
            os.remove(fl)

# def uploadVideo(dic,fl,bucket):
#     meta = dic['meta']
#     path = dic['path']
#     filename = path[path.rfind("/") + 1:]
#     videoBlob = bucket.blob("videos/"+filename)
#     metadata  = {"firebaseStorageDownloadTokens": uuid.UUID(meta)}
#     # Set metadata to blob
#     videoBlob.metadata = metadata

#     logger.info(str(videoBlob.upload_from_filename(path)))
#     # delete the temporary file
#     os.remove(fl)
#     os.remove(path)



# def uploadOfflineEvents(fs):
#     if fs is None:  
#         logger.info(u"[offline] Fs is none")
#         return
#     current_directory = os.getcwd()
#     logger.info(u"[offline] current_directory {}".format(str(current_directory)))
#     dirs = [f for f in glob(current_directory+'/.eJson/**', recursive=True) if os.path.isdir(f)]
#     logger.info(u"[offline] Found dirs {}".format(str(dirs)))
#     for ed in dirs:
#         ename = ed[ed.rfind("/") + 1:]
#         logger.info(u"ename {}".format(ename))
#         if ename != 'LoadEvents' and ename != 'VideoLink' :
#             logger.info(u"not found the event")
#             continue
#         upload = UploadLoad(fs) if ename == "LoadEvents" else UploadVLink(fs)
#         upload.uploadEvent(ed)



# class UploadDic(ABC):
#     def __init__(self,fs):
#         self.fs = fs
#     def uploadEvent(self, ed ):
#         files  = [f for f in glob(ed+'/**', recursive=True) if os.path.isfile(f)]
#         logger.info(u"[offline] uploading files {}".format(str(files)))
#         for fl in files:
#             with open(fl) as f:
#                 dic = json.load(f)
#                 t= threading.Thread(target=self.upload,args=(dic,fl))
#                 t.start()

#     @abstractmethod
#     def upload(self,dic,fl):
#         pass

# class UploadLoad(UploadDic):
#     def __init__(self, fs):
#         super().__init__(fs)
#     def upload(self, dic,fl):
#         logger.info(u"[offline] uploading load Event"+str(dic))
#         self.fs.uploadEventDic(dic)
#         os.remove(fl)
#         return super().upload(dic,fl)

# class UploadVLink(UploadDic):
#     def __init__(self, fs):
#         super().__init__(fs)
#     def upload(self, dic,fl):
#         logger.info(u"[offline] uploading vLink Event"+str(dic))
#         self.fs.uploadVLinkDic(dic)
#         os.remove(fl)
#         return super().upload(dic,fl)






    

