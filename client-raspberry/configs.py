from log import *
import argparse
from pyimagesearch.utils import Conf
from util import getserial



class Configs:
    def __init__(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-c", "--conf", required=True,
            help="Path to the input configuration file")
        ap.add_argument("-dv", "--delv",  action="store_true",
            help="Delete Video cache (Y/N)")
        args = vars(ap.parse_args())
        logger.info(u"Configs are {}".format(args))
        conf = Conf(args["conf"])
        self.truckId= conf["truckId"]
        self.picamera= conf["picamera"]
        self.camRotate180= conf["camRotate180"]
        self.camRotate90= conf["camRotate90"]
        self.camRotateC90= conf["camRotateC90"]
        self.automeanCal= conf["automeanCal"]
        self.truckenvithresh= conf["truckenvithresh"]
        self.open_threshold_seconds= conf["open_threshold_seconds"]
        self.sms_to= conf["sms_to"]
        self.session_duration=conf["session_duration"]
        self.confidence= conf["confidence"]
        self.serialNum = conf["defaul_sl"]
        self.camRotate180 = conf["camRotate180"]
        self.camRotate90 = conf["camRotate90"]
        self.camRotateC90 = conf["camRotateC90"]

        sl = getserial()
        if sl != 'unknown':
            self.serialNum = sl
        print(u'device serial = {}'.format(self.serialNum))
    
    def update(self,args=''):
        if args is None and args == '':
            logger.info("Empty config update")
        else :
            logger.info(u'Updating config for args {}'.format(args))
            arr = args.split(":")
            if arr is None and arr.length < 2:
                logger.info("Not able to parse cofig args")
            else :
                key = arr[0]
                value = arr[1]
                self.u(key)(value)
                
    def u(self,x):
        return {
            'truckId': self.updateTruckId,
            'truckenvithresh': self.updateTruckenvithresh,
            'sms_to': self.updatePhNum,
            'camRotate180': self.updateCamRotate180,
            'camRotate90': self.updateCamRotate90,
            'camRotateC90': self.updateCamRotateC90

        }[x]

    def updateCamRotate180(self, id):
        if id is None and id == '':
            logger.info('updateCamRotate180 Invalid truck id')
        else :
            logger.info('Updating the updateCamRotate180 {}'.format(id))
            if id == 'true' :
                self.camRotate180 = True
            else :
                self.camRotate180 = False

    def updateCamRotate90(self, id):
        if id is None and id == '':
            logger.info('updateCamRotate90 Invalid truck id')
        else :
            logger.info('Updating the updateCamRotate90 {}'.format(id))
            if id == 'true' :
                self.camRotate90 = True
            else :
                self.camRotate90 = False
    
    def updateCamRotateC90(self, id):
        if id is None and id == '':
            logger.info('camRotateC90 Invalid truck id')
        else :
            logger.info('Updating the camRotateC90 {}'.format(id))
            if id == 'true' :
                self.camRotateC90 = True
            else :
                self.camRotateC90 = False
    

    def updateTruckId(self, id):
        if id is None and id == '':
            logger.info('Invalid truck id')
        else :
            logger.info('Updating the truck id {}'.format(id))
            self.truckId = id
    
    def updateTruckenvithresh(self, id):
        if id is None and id == 0:
            logger.info('Invalid truckenvithresh ')
        else :
            logger.info('Updating the truckenvithresh {}'.format(id))
            self.truckenvithresh = id

    def updatePhNum(self, sms_to):
        if sms_to is None and sms_to == 0:
            logger.info('Invalid sms_to ')
        else :
            logger.info('Updating the sms_to {}'.format(sms_to))
            self.sms_to = sms_to


    def updateConfidence(self, confidence):
        if confidence is None and confidence == 0:
            logger.info('Invalid confidence ')
        else :
            logger.info('Updating the confidence {}'.format(confidence))
            self.confidence = confidence
    
    


