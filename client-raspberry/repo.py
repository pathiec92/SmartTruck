from google.cloud import storage
from firebase import firebase
import os
import requests
from datetime import datetime
import uuid
from firestore_service import FireStoreService
from offline import *
from log import *

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="MyCloudStorage-3e526dc49133.json"
firebase = firebase.FirebaseApplication('https://mycloudstorage-1135.appspot.com')
#phNum = "8970151515"
#vehicleNum = "KA03 HM2345"

class Gcloud:
    def __init__(self, conf, fservice:FireStoreService):
        self.phNum = conf["sms_to"]
        self.vehicleNum = fservice.configs.truckId
        self.fservice = fservice
        self.offlineWorker = OfflineWorker(self.uploadOffline,self.notifyOnline)
        self.bucket = None
        if isConnected():
            self.initBucketIfNot()
       
    def notifyOnline(self):
        self.initBucketIfNot()

    def initBucketIfNot(self):
        if self.bucket is None:
            while self.fservice.shouldRunService is False :
                time.sleep(1)
            self.bucket = storage.Client().get_bucket('mycloudstorage-1135.appspot.com')
        
    def uploadOffline(self,tempVideo):
        logger.info(u"[Gcloud] uploading offline {}".format(tempVideo.path))
        t= threading.Thread(target=self.upload,args=(tempVideo,True))
        t.start()
       # self.upload(tempVideo)

    def upload(self, tempVideo, isSendMessage=False, slotStartTime=datetime.now()):
        logger.info(u"Uploading the file {}".format(tempVideo.path))
        # Create new token
        new_token = uuid.uuid4()
        # Create new dictionary with the metadata
        metadata  = {"firebaseStorageDownloadTokens": new_token}
        filename = tempVideo.path[tempVideo.path.rfind("/") + 1:]

        if isConnected() is False:
            self.offlineWorker.saveVLink(tempVideo.path, new_token)
        else :
            self.initBucketIfNot()
            videoBlob = self.bucket.blob("videos/"+filename)
            # Set metadata to blob
            videoBlob.metadata = metadata
            logger.info(str(videoBlob.upload_from_filename(tempVideo.path)))
            # delete the temporary file
            tempVideo.cleanup()
            logger.info(videoBlob.public_url)
            self.sendSms(filename, new_token, isSendMessage, slotStartTime)
        
        return "videoBlob.public_url"

    def sendSms(self,name,token, isSendMessage,slotStartTime):
        #downloadLink = u"https%3A%2F%2Ffirebasestorage.googleapis.com%2Fv0%2Fb%2Fmycloudstorage-1135.appspot.com%2Fo%252Fvideos%25{}%3Falt%3Dmedia%26token%3D{}".format(name,token)
        downloadSMSLink = u"https://firebasestorage.googleapis.com/v0/b/mycloudstorage-1135.appspot.com/o/videos%252F{}?alt=media%26token={}".format(name,token)
        downloadLink = "https://firebasestorage.googleapis.com/v0/b/mycloudstorage-1135.appspot.com/o/videos%2F{}?alt=media&token={}".format(name,token)
        startTime = slotStartTime.strftime("%I:%M:%S%p")
        logger.info(u"Opened At {}".format(startTime))
        msgSMS = u"Your Vehicle No. {} Door Opened at {} and you can view/ download video clip at {}".format(self.fservice.configs.truckId, startTime, downloadSMSLink)
        msg = u"Your Vehicle No. {} Door Opened at {} and you can view/ download video clip at {}".format(self.fservice.configs.truckId, startTime, downloadLink)
        sms = u"https://www.businesssms.co.in/sms.aspx?ID=satyology@gmail.com&Pwd=Nastssms@2328&PhNo={}&Text={}" \
        .format(self.phNum, msgSMS)
        logger.info(u'fservice truckId {}'.format(self.fservice.configs.truckId))
        if(isSendMessage):
            logger.info(u"Sending sms {}".format(sms))
            r = requests.get(sms)
            logger.info(u"request = {}".format(r))
        else :
            logger.info(u"Motion is detected, but not sure if human")

        self.fservice.uploadEvent(msg,"danger")
        self.fservice.uploadVLink(downloadLink)
        #logger.info(u"desc = {}, status = {}, header = {}".format( r.json()["description"], r.status_code, r.headers['content-type']))

