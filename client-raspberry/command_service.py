from log import *
from firestore_service import *
from configs import *

class Command:
     def __init__(self, truckId, fStore, configs):
        self.commands:""
        self.restartCommand = RestartCommand()
        self.nullCommand = NullCommand()
        self.truckId = truckId
        self.fStore = fStore
        self.updateConfig = UpdateConfigCommand(configs)
        return
    
     def serve(self, doc_snapshot, changes, read_time):
         print(u'received command document {0}'.format(doc_snapshot))
         logger.info(u'received command document {0}'.format(doc_snapshot))
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
        if command == 'restart':
            return self.restartCommand
        elif command == 'configs' :
            return self.updateConfig
        else :
            return self.nullCommand




class InFaceCommand:
    def execute(self,args=""):
        return

class NullCommand(InFaceCommand):
    def execute(self, args=''):
        logger.info("Invalid command")
        return super().execute(args=args)

    

class RestartCommand (InFaceCommand):
    def execute(self, args=''):
        logger.info('Restarting app')
        return super().execute(args=args)

class UpdateConfigCommand(InFaceCommand):
    def __init__(self, configs):
        super().__init__()
        self.configs = configs

    def execute(self, args=''):
        logger.info('Updating the config')
        self.configs.update(args)
        return super().execute(args=args)



