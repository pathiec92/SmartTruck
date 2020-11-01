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
        print(u'An exception occurred while parsing the time string {}'.format(str))
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
ap.add_argument("-s", "--start", 
	help="Start date is required")
# ap.add_argument("-e", "--end",  required=True,
# 	help="End date is required")

args = vars(ap.parse_args())
start=0
end= 0
if parse(args, "start") is not None:
    start= convert(args["start"]+'T00:00:01.807+00:00')
if parse(args, "start") is not None:
    end= convert(args["start"]+'T23:59:58.807+00:00')

# print(time.time())
# print(datetime.now())



print(start)
print(end)

pr = PullReport(start, end)
pr.pull()
c = 100
while True and c > 0:
    time.sleep(0.25)
    c -= 1
pr.stichAndPrint()

print('Generated cambot report successfully')



