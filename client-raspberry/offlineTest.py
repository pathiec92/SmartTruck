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
# pr.stichAndPrint()
ap = argparse.ArgumentParser()

ap.add_argument("-f", "--folder", required=True,
                help="Specify the root folder")
args = vars(ap.parse_args())

destFolder = args["folder"]

for root, subFolders, files in os.walk(os.getcwd()+'/'+destFolder):
    videosFolder = ''
    if os.path.isdir(root) is True:
        #print('--root :{}, subFolders: {}, files: {}'.format(root,subFolders,files))
        vid = os.path.basename(root)
        if vid == 'videos' and os.path.isdir(root):
            print('is vid path:'+ vid)
            #print(u'directory {}'.format(root))
            for f in files:
                vf = root+'/'+f
                print('video :' + vf)
