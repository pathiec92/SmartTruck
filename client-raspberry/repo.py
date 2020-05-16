from google.cloud import storage
from firebase import firebase
import os
import requests
from datetime import datetime
from uuid import uuid4

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="MyCloudStorage-3e526dc49133.json"
firebase = firebase.FirebaseApplication('https://mycloudstorage-1135.appspot.com')
#phNum = "8970151515"
vehicleNum = "KA03 HM2345"

class Gcloud:
    def __init__(self, conf, fservice):
        self.phNum = conf["sms_to"]
        self.bucket = storage.Client().get_bucket('mycloudstorage-1135.appspot.com')
        self.fservice = fservice

    def upload(self, tempVideo):
        print(u"Uploading the file {}".format(tempVideo.path))
        filename = tempVideo.path[tempVideo.path.rfind("/") + 1:]
        videoBlob = self.bucket.blob("videos/"+filename)
        # Create new token
        new_token = uuid4()
        # Create new dictionary with the metadata
        metadata  = {"firebaseStorageDownloadTokens": new_token}
        # Set metadata to blob
        videoBlob.metadata = metadata

        print(str(videoBlob.upload_from_filename(tempVideo.path)))
        self.sendSms(filename, new_token)
        # delete the temporary file
        tempVideo.cleanup()
        print(videoBlob.public_url)
        return videoBlob.public_url

    def sendSms(self,name,token):
        #downloadLink = u"https%3A%2F%2Ffirebasestorage.googleapis.com%2Fv0%2Fb%2Fmycloudstorage-1135.appspot.com%2Fo%252Fvideos%25{}%3Falt%3Dmedia%26token%3D{}".format(name,token)
        downloadLink = u"https://firebasestorage.googleapis.com/v0/b/mycloudstorage-1135.appspot.com/o/videos%252F{}?alt=media%26token={}".format(name,token)
        startTime = datetime.now().strftime("%I:%M:%S%p")
        print(u"Opened At {}".format(startTime))
        msg = u"Your Vehicle No. {} Door Opened at {} and you can view/ download video clip at {}".format(vehicleNum, startTime, downloadLink)
        sms = u"https://www.businesssms.co.in/sms.aspx?ID=satyology@gmail.com&Pwd=Nastssms@2328&PhNo={}&Text={}" \
        .format(self.phNum, msg)
        print(u"Sending sms {}".format(sms))
        r = requests.get(sms)
        self.fservice.uploadEvent(msg,"danger")
        #print(u"desc = {}, status = {}, header = {}".format( r.json()["description"], r.status_code, r.headers['content-type']))
        print(u"request = {}".format( r))

