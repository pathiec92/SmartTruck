import requests
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import time
import re
from datetime import datetime

videosFolder=""
executor = ThreadPoolExecutor(5)


def getFilename_fromCd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

def downloadTask(url):
    r = requests.get(url, allow_redirects=True)
    destFile = getFilename_fromCd(r.headers.get('content-disposition'))
    if destFile is None:
        destFile= videosFolder+'/'+ str(time.time())+'.avi'
    else:
        destFile = videosFolder+'/'+destFile

    open(destFile, 'wb').write(r.content)
    return url


def download(url,destFile):
    createDir(destFile)
    print(u'Downloading from url {}, dest folder = {}'.format(url, destFile))
    future = executor.submit(downloadTask, url)
    print(future.done())
    print(future.result())
    print(future.done())
    print('Waiting for download to complete')
    return future


def createDir(folderName):
        path = ""
        current_directory = os.getcwd()
        path = os.path.join(current_directory, folderName)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

# for i in range(10):
#     url = 'http://google.com/favicon.ico'
#     r = requests.get(url, allow_redirects=True)
#     executor = ThreadPoolExecutor(5)
#     future = executor.submit(download, (url))
#     print(future.done())
#     print(future.result())
def downloadVideos():
    folder = ''
    for root, subFolders, files in os.walk(os.getcwd()+'/report'):
        print(root)
        
        print('--files')
        videosFolder = ''
        if os.path.isdir(root) is True:
            print(u'directory {}'.format(root))
            folder = root
            videosFolder=folder+'/videos'
            
        for f in files:        
            print(f)
            if f == 'videoLinks.txt':
                createDir(videosFolder)
                vl = folder+'/videoLinks.txt'
                print(u'Download FileName.. {}'.format(vl))
                # urlArr = []
                # with open(vl) as my_file:
                #     urlArr = my_file.readlines()
                # with ThreadPoolExecutor(max_workers=5) as executor:
                #     res = executor.map(downloadTask, urlArr)
                # responses = list(res)
                # print('---------RESPONSES---------')
                # for i in responses:
                #     print(i)
                vf = open(vl)
                for url in vf:
                    #destFolder =videosFolder+'/'+ str(time.time())+'.avi'
                    print(u'{}: {}'.format(datetime.now(), downloadTask(url)))


downloadVideos()

while True:
    sleep(0.25)

#download('https://firebasestorage.googleapis.com/v0/b/mycloudstorage-1135.appspot.com/o/videos%2F7d703ac5-dada-4bab-a665-c58d960b16d2.avi?alt=media&token=1320e63f-90f0-462a-aeb7-875c172f1463','/home/zebra/SmartTruck/client-raspberry/report/HT2020100001/7c3217db-c10c-93d0-7549-218bf6eac8a1/videos')



print(os.path.isdir('/home/zebra/SmartTruck/client-raspberry/report/HT2020100002/8089e0c2-5426-a654-8175-34016fea297f'))
        


