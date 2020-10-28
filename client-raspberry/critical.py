
class Critical:
    def __init__(self, fservice):
       self.fservice = fservice
       self.process=fservice.instance

    def logc(self,msg):
        self.fservice.uploadEvent(msg,"danger")

    def log(self, msg, type="info"):
        self.fservice.uploadEvent(msg,type)




