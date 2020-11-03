import time
from datetime import datetime
from report_pull import *
import argparse

def convert(str):
    if str is None:
        return 0
    t = 0
    try:
        t = int(datetime.fromisoformat(str).timestamp() *1000)
    except:
        print(u'An exception occurred while parsing the time string {}, date format: YYYY:MM::DD'.format(str))
        t = time.time() * 1000
    return int(t)

def parse(ar, k):
    v=None
    try:
        v=ar[k]
    except:
        print('Exceptions')
    return v


ap = argparse.ArgumentParser()
ap.add_argument("-s", "--start", required=True,
	help="Start date is required in the format YYYY-MM-DD")
# ap.add_argument("-e", "--end",  required=True,
# 	help="End date is required")

args = vars(ap.parse_args())
start=0
end= 0
if parse(args, "start") is not None:
    start= float(convert(args["start"]+'T00:00:01.807+05:30'))
if parse(args, "start") is not None:
    end= float(convert(args["start"]+'T23:59:58.807+05:30'))

print(time.time())
print(datetime.now())



print(start)
print(end)

pr = PullReport(start, end)
pr.pull()
c = 2400
while pr.isOpDone() is False:
    time.sleep(0.25)
    c -= 1
print('1. isOpDone:{}, c:{}'.format(pr.isOpDone(), c))

c = 40
while c>0:
    time.sleep(0.25)
    c -= 1
    
print('1. isOpDone:{}, c:{}'.format(pr.isOpDone(), c))
#pr.stichAndPrint()

print('Generated cambot report successfully')



