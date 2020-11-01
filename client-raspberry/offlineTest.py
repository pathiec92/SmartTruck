import time
from datetime import datetime
from report_pull import *
import argparse
# pr = PullReport()
# pr.pull()
# c = 160
# while True and c > 0:
#     time.sleep(0.25)
#     c -= 1
#pr.stichAndPrint()
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--start", required=True,
	help="Start date is required")
ap.add_argument("-e", "--end",  required=True,
	help="End date is required")

args = vars(ap.parse_args())

start= args["start"]+'T00:00:01.807+00:00'
end= args["end"]+'T00:00:01.807+00:00'

print(time.time())
print(datetime.now())
def convert(str):
    t = 0
    try:
        t = int(datetime.fromisoformat(str).timestamp() *1000)
    except:
        print(u'An exception occurred while parsing the time string {}'.format(str))
    return t

print(convert('2020-11-01T00:00:01.807+00:00'))
print(convert('x'))
print(convert(start))
print(convert(end))



