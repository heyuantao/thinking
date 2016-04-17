from __future__ import unicode_literals
import youtube_dl
import os
import sys
import os

class DownloadLogger(object):
    def debug(self, msg):
        pass
        #print "Debug:",msg

    def warning(self, msg):
        pass
        #print "Warning:",msg

    def error(self, msg):
        pass
        #print "Error:",msg


def DownloadProcessHook(d):
    #print d
    print "in loop pid:%s"%(os.getpid())
    if d['status'] == 'finished':
        print('Done downloading !')
    if d['status'] == 'downloading':
        precent=d['_percent_str']
        print "Precent %s" %(precent)
class YoutubeDownload(object):
    def __init__(self,link):
        self.link=link
        self.ydl_opts = {
                    'proxy':'localhost:1080',
                    'no-playlist':True,
                    'logger':DownloadLogger(),
                    'progress_hooks': [DownloadProcessHook],
        }
    def beginDownload(self):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.link])

def main():
    listFileName="videoListFile.txt"
    file=open(listFileName)
    downloadLinkList=[]
    for line in file:
        downloadLinkList.append(line.strip())
    file.close()
    print "Number of item to download:%d" %(len(downloadLinkList))
    for item in downloadLinkList:
        downloadItem=YoutubeDownload(item)
        print "Begin download:",item
        downloadItem.beginDownload()

if __name__=="__main__":
    print "system pid:%s" %(os.getpid())
    main()