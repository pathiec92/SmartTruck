from google.cloud import storage
from firebase import firebase
import os
import requests
from datetime import datetime
import uuid
from offline import *
from log import *
import os.path
from os import path

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="MyCloudStorage-3e526dc49133.json"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="smarttruck-8a93a-c7f7019ed403.json"
#firebase = firebase.FirebaseApplication('https://mycloudstorage-1135.appspot.com')
firebase = firebase.FirebaseApplication('https://smarttruck-8a93a.appspot.com')


#phNum = "8970151515"
#vehicleNum = "KA03 HM2345"

class Gcloud:
    def __init__(self, fservice):
        self.phNum = fservice.configs.sms_to
        self.vehicleNum = fservice.configs.truckId
        self.fservice = fservice
        self.offlineWorker = OfflineWorker(self.uploadOffline,self.notifyOnline)
        self.bucket = None
        if isConnected():
            self.initBucketIfNot()
        print(u'Gcloud ct')

    def notifyOnline(self):
        self.initBucketIfNot()

    def initBucketIfNot(self):
        if self.bucket is None:
            tryCount = 5
            while self.fservice.shouldRunService is False and tryCount>0 :
                tryCount -= 1
                time.sleep(1)
            self.bucket = storage.Client().get_bucket('smarttruck-8a93a.appspot.com')
        
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
            if path.exists(tempVideo.path):    
                try:
                    logger.info(str(videoBlob.upload_from_filename(tempVideo.path)))
                    logger.info(videoBlob.public_url)
                    self.sendSms(filename, new_token, isSendMessage, slotStartTime)
                except:
                    logger.info(u"Error while uploading the file {}".format(tempVideo.path)) 

            # delete the temporary file
                tempVideo.cleanup()
            
        
        return "videoBlob.public_url"

    

    def sendSms(self,name,token, isSendMessage,slotStartTime):
        #downloadLink = u"https%3A%2F%2Ffirebasestorage.googleapis.com%2Fv0%2Fb%2Fmycloudstorage-1135.appspot.com%2Fo%252Fvideos%25{}%3Falt%3Dmedia%26token%3D{}".format(name,token)
        downloadSMSLink = u"https://firebasestorage.googleapis.com/v0/b/smarttruck-8a93a.appspot.com.com/o/videos%252F{}?alt=media%26token={}".format(name,token)
        downloadLink = "https://firebasestorage.googleapis.com/v0/b/smarttruck-8a93a.appspot.com/o/videos%2F{}?alt=media&token={}".format(name,token)
        startTime = slotStartTime.strftime("%I:%M:%S%p")
        logger.info(u"Opened At {}".format(startTime))
        msgSMS = u"CamBot: Your Truck No. {} Door Opened at {} and you can view/ download video clip at {} - Satyology Solutions".format(self.fservice.configs.truckId, startTime, downloadSMSLink)
        msg = u"CamBot: Your Truck No. {} Door Opened at {} and you can view/ download video clip at {} - Satyology Solutions".format(self.fservice.configs.truckId, startTime, downloadLink)
        #msgSMS = u"CamBot: Your Truck No. {} Door Opened/ Activity at {} and you can view/ download video clip at Link from Satyology Solutions".format(self.fservice.configs.truckId, startTime)
        #sms = u"https://www.businesssms.co.in/sms.aspx?ID=satyology@gmail.com&Pwd=Nastssms@2328&PhNo={}&Text={}" \
        sms = u"https://www.businesssms.co.in/sms.aspx?ID=satyology@gmail.com&Pwd=Cambot@242328&PhNo={}&Text={}&TemplateID=1007319788716414928" \
        .format(self.phNum, msgSMS)
        #sms = u"https://www.businesssms.co.in/sms.aspx?ID=satyology@gmail.com&Pwd=Nastssms@2328&PhNo={}&Text={}&TemplateID=100739476470270232" \
        #.format(self.phNum, msgSMS)
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

    def uploadLogEvent(self,fileNames:[],logId):
        links = []
        for name in fileNames :
            links.append("https://firebasestorage.googleapis.com/v0/b/smarttruck-8a93a.appspot.com/o/logs%2F{}%2F{}?alt=media&token={}".format(self.fservice.configs.truckId,name,logId))
        startTime = datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")
        logger.info(u"logs collected At {}".format(startTime))
        logEvent = {
            u'logId': logId,
            u'truckId': self.fservice.configs.truckId,
            u'links': links,
            u'at': startTime
        }
        logger.info(u'Uploading the log event {}'.format(logEvent))
        self.fservice.uploadLogLinkDic(logEvent,logId)

    def uploadLogFile(self, tempVideo, logId):
        logger.info(u"Uploading the log file {}".format(tempVideo.path))
        # Create new dictionary with the metadata
        metadata  = {"firebaseStorageDownloadTokens": logId}
        filename = tempVideo.path[tempVideo.path.rfind("/") + 1:]
        self.initBucketIfNot()
        videoBlob = self.bucket.blob("logs/"+self.fservice.configs.truckId+"/"+filename)
        # Set metadata to blob
        videoBlob.metadata = metadata
        logger.info(str(videoBlob.upload_from_filename(tempVideo.path)))
        logger.info(u"log upload to :{}".format(videoBlob.public_url))

