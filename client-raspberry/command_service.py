from log import *
from firestore_service import *
from configs import *
import threading
from slot import *
import os
from logupload import LogUpload
from repo import Gcloud



diagInstance = "diag"
mainInstance = "main"
class Command:
     def __init__(self, truckId, fStore, configs):
        print('Creating the command')
        self.commands:""
        self.restartCommand = RestartCommand()
        self.rebootCommand = RebootCommand()
        self.previewCommand = PreviewCommand()

        self.nullCommand = NullCommand()
        self.truckId = truckId
        self.fStore = fStore
        self.gCloud = Gcloud(fStore)
        self.updateConfig = UpdateConfigCommand(configs)
        self.logUploadCommand = LogUploadCommand(self.gCloud)
        
        return
    
     def serve(self, doc_snapshot, changes, read_time):
        # print(u'received command document {0}'.format(doc_snapshot))
         #logger.info(u'received command document {0}'.format(doc_snapshot))
         for doc in doc_snapshot:
            logger.info(u'Serving command : {} => {}'.format(doc.id, doc.to_dict()))
            print(u'Serving command : {} => {}'.format(doc.id, doc.to_dict()))
            command = doc.to_dict().get("command")
            logger.info(u'command = {}'.format(command))
            args = doc.to_dict().get("args")
            logger.info(u'args = {}'.format(args))
            ack = doc.to_dict().get("ack")
            if ack is None or ack == '':
                now = int(round(time.time() * 1000))
                cdDic = {
                    u'truckId' : self.truckId,
                    u'command': command,
                    u'args': args,
                    u'ack': "ack",
                    u'at':now
                }
                self.fStore.updateCommand(cdDic)
                cmd = self.getCommand(command)
                cmd.execute(args)
                
            else :
                logger.info('command {}({}) already executed'.format(command, args))


     def getCommand(self, command):
        logger.info(u'serving command instance {}'.format(self.fStore.instance))
        if command == 'restart' and self.fStore.instance == diagInstance:
            return self.restartCommand
        if command == 'reboot' and self.fStore.instance == diagInstance:
            return self.rebootCommand
        if command == 'preview' and self.fStore.instance == diagInstance:
            return self.previewCommand            
        if command == 'logs' and self.fStore.instance == diagInstance:
            return self.logUploadCommand
        elif command == 'configs' :
            return self.updateConfig
        else :
            return self.nullCommand

def onSlotComplete(duration):
    print('Command service onSlotComplete')

slt = slot(onSlotComplete)


class InFaceCommand:
    def execute(self,args=""):
        return

class NullCommand(InFaceCommand):
    def execute(self, args=''):
        logger.info("Invalid command")
        return super().execute(args=args)

    

class RestartCommand (InFaceCommand):
    def execute(self, args=''):
        logger.info(u'Human Detection Service will restart in 10 seconds')
        t= threading.Thread(target=slt.schedule,args=(10, self.restartDevice))
        t.start()  
        return super().execute(args=args)
    
    def restartDevice(self):
       logger.info('Restarting The Human Detect Service')
       os.system('ps axf | grep human_detect | grep -v grep | awk \'{print \"kill -9 \" $1}\' | sh')
       print('Starting human-detection')
	   #os.system('cd /home/satyol/cambot; python3 human_detect.cpython-37.pyc -c config/config.json')
       os.system('cd ~/SmartTruck/client-raspberry; python3 human_detect.py -c config/config.json')

class PreviewCommand (InFaceCommand):
    def execute(self, args=''):
        if args == 'start':
            os.system('ps axf | grep human_detect | grep -v grep | awk \'{print \"kill -9 \" $1}\' | sh')
            logger.info(u'Device will preview in 15 seconds')
            print('Device will preview in 15 seconds')
            t= threading.Thread(target=slt.schedule,args=(15, self.previewDevice))
            t.start()        
            return super().execute(args=args)
        elif args == 'stop':
           os.system('ps axf | grep webstreaming | grep -v grep | awk \'{print \"kill -9 \" $1}\' | sh')
           logger.info(u'Cambot Preview Ended')
           return super().execute(args=args)
    
    def previewDevice(self):
        logger.info(u'Previewing Device')
        print('Previewing Device')
        os.system('cd /home/satyol/video_surveillance; python3 webstreaming.py --ip 192.168.0.61 --port 8000')
        #os.system('cd ~/SmartTruck/client-raspberry/video_surveillance; python3 webstreaming.py --ip 192.168.0.61 --port 8000')


class RebootCommand (InFaceCommand):
    def execute(self, args=''):
        logger.info(u'Device will reboot in 15 seconds')
        t= threading.Thread(target=slt.schedule,args=(15, self.rebootDevice))
        t.start()        
        return super().execute(args=args)
    
    def rebootDevice(self):
        logger.info(u'Rebooting Device')
        os.system('reboot')

class LogUploadCommand (InFaceCommand):
    def __init__(self, gCloud):
        super().__init__()
        print(u'LogUploadCommand  created')
        self.logupload = LogUpload(gCloud)
         

    def execute(self, args=''):
        logger.info(u'Command: Uploading the logs')
        logargs = args.split('$')
        logNum = 0
        logId = "temp"
        if len(logargs)>1 :
            logId = logargs[0]
            logNum = int(logargs[1])

        self.logupload.uploadLogs(logId, logNum)
        return super().execute(args=args)
        


class UpdateConfigCommand(InFaceCommand):
    def __init__(self, configs):
        super().__init__()
        self.configs = configs

    def execute(self, args=''):
        logger.info('Updating the config')
        self.configs.update(args)
        return super().execute(args=args)



