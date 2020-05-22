from repo import *
from datetime import datetime
from datetime import date

cloud = Gcloud()

startTime = datetime.now()
print(u"startTime = {}".format(startTime))
dateOpened = date.today().strftime("%A, %B %d %Y")
print(u"dateOpened = {}".format(dateOpened))

print(u"startTime = {}".format(startTime.strftime("%I:%M%p")))

cloud.sendSms("https://firebasestorage.googleapis.com/v0/b/mycloudstorage-1135.appspot.com/o/videos%2F1cd600b8-56d7-49b0-854f-48d972f69f4c.avi?alt=media&token=785a22d1-8592-49c7-8c1e-7610ed0851ec")