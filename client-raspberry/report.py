class Truck:
    def __init__(self,truckId):
        self.truckId = truckId
        self.loadIdDic = {}
        
class Load:
    def __init__(self,loadId):
        self.loadId = loadId
        self.loadEvent = []
        self.videoEvent = set()