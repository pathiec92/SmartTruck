from report_fb import *
import argparse
class PullReportForId:
    def __init__(self,id, start, end):
        print(u'PullReportForId id:{}, start:{}, end:{}'.format(id, start, end))
        self.start = start
        self.end = end
        self.id = id
        self.fservice = FireReportService(start, end)
        #self.fservice = FireReportService(self.start,self.end)


    def pull(self):
       #self.fservice.subscribeTruckId()
       self.fservice.subscribe(self.id)
       #self.fservice.subLoadVideo("HT2020100008", "10000000a49e76f6", "7460ac46-3fe6-a169-f374-5e30173903ec")
    def isRecordPulled(self):
        return self.fservice.isRecordPulled()

    def stichAndPrint(self):
        self.fservice.stichReportNPrint()
        #self.fservice.printReport()
        self.fservice.writeReport()

    def createDir(self, folderName):
        path = ""
        current_directory = os.getcwd()
        path = os.path.join(current_directory, folderName)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

ap = argparse.ArgumentParser()
ap.add_argument("-id", "--id", required=True,
	help="TruckId must be there")
ap.add_argument("-s", "--start", required=True,
	help="Start date in millisec is required")
ap.add_argument("-e", "--end", required=True,
	help="End date in millisec is required")

args = vars(ap.parse_args())


pri = PullReportForId(args['id'], int(args['start']), int(args['end']))
pri.pull()
c = 50
while c > 0 and pri.isRecordPulled() is False:
    time.sleep(0.25)
    c -= 1
print('1.[Report] isOpDone:{}, c:{}'.format(pri.isRecordPulled(), c))
c = 50
while c > 0 and pri.isRecordPulled() is False:
    time.sleep(0.25)
    c -= 1
print('2.[Report] isOpDone:{}, c:{}'.format(pri.isRecordPulled(), c))

pri.stichAndPrint()




            

