import requests
import os
import threading

from time import sleep
import time
import re
from datetime import datetime
from multiprocessing.pool import ThreadPool

videosFolder=""


def gestDest(videosFolder):
    destFile= videosFolder+'/'+ str(time.time())+'.avi'
    return destFile
    
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
def fetch_url(entry):
    path, uri = entry
    uri = uri.strip()
    print(u'fetch_url {}, {}, {}'.format(path, uri,os.path.exists(path) ))

    if not os.path.exists(path):
        r = requests.get(uri, stream=True)
        print('----------status_code-:{}, {}'.format(r.status_code, uri))
        if r.status_code == 200:
            print('----------Downloading-:{}'.format(uri))
            with open(path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
    return path

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
        urlArr = [] 
        for f in files:        
            print(f)
            if f == 'videoLinks.txt':
                createDir(videosFolder)
                vl = folder+'/videoLinks.txt'
                print(u'Download FileName.. {}'.format(vl))
                
                with open(vl) as my_file:
                    for line in my_file:
                        urlTople = (gestDest(videosFolder), line)
                        urlArr.append(urlTople)
        results = ThreadPool(2).imap_unordered(fetch_url, urlArr)

        for path in results:
            print(path)





downloadVideos()

# while True:
#     sleep(0.25)

#fetch_url(('/home/zebra/SmartTruck/client-raspberry/report/HT2020100001/7c3217db-c10c-93d0-7549-218bf6eac8a1/videos/x.avi','https://firebasestorage.googleapis.com/v0/b/mycloudstorage-1135.appspot.com/o/videos%2F7d703ac5-dada-4bab-a665-c58d960b16d2.avi?alt=media&token=1320e63f-90f0-462a-aeb7-875c172f1463'))



print(os.path.isdir('/home/zebra/SmartTruck/client-raspberry/report/HT2020100002/8089e0c2-5426-a654-8175-34016fea297f'))
        


