from google.cloud import storage
from firebase import firebase
import os
import requests
from datetime import datetime
import uuid
from firestore_service import FireStoreService
from offline import *

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="MyCloudStorage-3e526dc49133.json"
firebase = firebase.FirebaseApplication('https://mycloudstorage-1135.appspot.com')
#phNum = "8970151515"
#vehicleNum = "KA03 HM2345"

class Gcloud:
    def __init__(self, conf, fservice:FireStoreService):

        self.phNum = conf["sms_to"]
        self.vehicleNum = conf["truckId"]
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
        print("[Gcloud] uploading offline {}".format(tempVideo.path))
        self.upload(tempVideo)

    def upload(self, tempVideo, isSendMessage):
        print(u"Uploading the file {}".format(tempVideo.path))
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
            print(str(videoBlob.upload_from_filename(tempVideo.path)))
            # delete the temporary file
            tempVideo.cleanup()
            print(videoBlob.public_url)
            self.sendSms(filename, new_token, isSendMessage)
        
        return "videoBlob.public_url"

    def sendSms(self,name,token, isSendMessage):
        #downloadLink = u"https%3A%2F%2Ffirebasestorage.googleapis.com%2Fv0%2Fb%2Fmycloudstorage-1135.appspot.com%2Fo%252Fvideos%25{}%3Falt%3Dmedia%26token%3D{}".format(name,token)
        #downloadLink = u"https://firebasestorage.googleapis.com/v0/b/mycloudstorage-1135.appspot.com/o/videos%252F{}?alt=media%26token={}".format(name,token)
        downloadLink = u"https://firebasestorage.googleapis.com/v0/b/mycloudstorage-1135.appspot.com/o/videos%2F{}?alt=media&token={}".format(name,token)
        startTime = datetime.now().strftime("%I:%M:%S%p")
        print(u"Opened At {}".format(startTime))
        msg = u"Your Vehicle No. {} Door Opened at {} and you can view/ download video clip at {}".format(self.vehicleNum, startTime, downloadLink)
        sms = u"https://www.businesssms.co.in/sms.aspx?ID=satyology@gmail.com&Pwd=Nastssms@2328&PhNo={}&Text={}" \
        .format(self.phNum, msg)
        if(isSendMessage):
            print(u"Sending sms {}".format(sms))
            r = requests.get(sms)
        else :
            print(u"Motion is detected, but not sure if human")

        print(u"request = {}".format( r))
        self.fservice.uploadEvent(msg,"danger")
        self.fservice.uploadVLink(downloadLink)
        #print(u"desc = {}, status = {}, header = {}".format( r.json()["description"], r.status_code, r.headers['content-type']))

