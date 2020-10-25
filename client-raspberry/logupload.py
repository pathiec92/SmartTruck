import time
import os 
from glob import glob
import threading
from imutils.io import TempFile

class LogUpload:
    def __init__(self,gCloud ):
        self.gCloud = gCloud
        return
    def uploadLogs(self,logId = "temp", count = 0):     
        #files  = [f for f in glob(os.getcwd()+'/logs/**', recursive=True) if os.path.isfile(f)]
        #logger.info(u"[Log] uploading files {}".format(str(files)))
        uploadCount = 2
        fold=os.getcwd()+'/logs/'
        fileNames=[]
        for x in range(uploadCount):
            if count == 0:
                path = u'{}smart_truck.log'.format(fold, )
            else :
                path = u'{}smart_truck.log.{}'.format(fold, count)
            count += 1
            if os.path.isfile(path) :
                print(u'uploading the log file  {} for id = {}'.format(path,logId))
                temp = TempFile()
                temp.path = path
                t= threading.Thread(target=self.gCloud.uploadLogFile,args=(temp,logId))
                t.start()
                fileName =  temp.path[temp.path.rfind("/") + 1:]
                fileNames.append(fileName)
        t1= threading.Thread(target=self.gCloud.uploadLogEvent,args=(fileNames,logId))
        t1.start()
                
        
                