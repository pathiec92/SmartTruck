from report_fb import *
class PullReport:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.fservice = FireReportService()
        #self.fservice = FireReportService(self.start,self.end)


    def pull(self):
       self.fservice.subscribeTruckId()

    def stichAndPrint(self):
        self.fservice.stichReportNPrint()
        #self.fservice.printReport()
        self.fservice.writeReport()

    def stichReportNPrint(self):
        for truckId in self.fservice.truckDic:
            truck = self.fservice.truckDic[truckId]
            for loadId in truck.loadIdDic:
                localLoad = self.fservice.localLoadIdDic[loadId]
                truck.loadIdDic[loadId] = localLoad

    def printReport(self):
        main = 'report'
        for truckId in self.fservice.truckDic:
            truck = self.fservice.truckDic[truckId]
            self.createDir(main+'/'+truckId)
            print(u'--> Truck :{}'.format(truckId))

            for loadId in truck.loadIdDic:
                load = truck.loadIdDic[loadId]
                self.createDir(main+'/'+truckId +'/'+ loadId)
                print(u'----> Load :{}'.format(loadId))

                print(u'<---- Load Events ---->')
                loadEventsPath = main+'/'+truckId +'/'+ loadId +'/loadEvents'
                #self.createDir(loadEventsPath)
                for l in load.loadEvent:
                    print(u'------> le :{}'.format(l))
                    with open(loadEventsPath,'w') as f:
                        f.write(l)


                print(u'<---- Video Events ---->')
                videoLinksPath = main+'/'+truckId +'/'+ loadId +'/videoLinks'
                #self.createDir(videoLinksPath)
                for l in load.videoEvent:
                    print(u'------> ve :{}'.format(l))
                    with open(loadEventsPath,'w') as f:
                        f.write(l)

    def createDir(self, folderName):
        path = ""
        current_directory = os.getcwd()
        path = os.path.join(current_directory, folderName)
        if not os.path.exists(path):
            os.makedirs(path)
        return path




            

