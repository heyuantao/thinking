import thread
import threading
import time
from WebSiteStatus import WebSiteStatus

#design pattern begin        
def singleton(class_):
  instances = {}
  def getinstance(*args, **kwargs):
    if class_ not in instances:
        instances[class_] = class_(*args, **kwargs)
    return instances[class_]
  return getinstance
#design pattern end

'''
class WebSiteStatusService(object):
    def __init__(self):
        self.urlList=[]
        self.runStatus=False
        self.locker=threading.Lock()
        
    def setUrlList(self,urlList):
        self.locker.acquire()
        self.urlList=urlList
        self.locker.release()
        
    def addUrlList(self,oneUrl):
        self.locker.acquire()
        self.urlList.append(oneUrl)
        self.locker.release()
        
    def backgroundThread(self):
        while True:
            if self.runStatus==False:
                break
            time.sleep(5)
            self.locker.acquire()
            cachedUrlList=[item for item in self.urlList]
            self.locker.release()
            webSiteStatus=WebSiteStatus()
            print cachedUrlList
            for oneUrl in cachedUrlList:                
                webSiteStatus.addSiteUrl(oneUrl)
            webSiteStatus.checkAll()
            webSiteStatus.displayAllStatus()
            
    def startTask(self):
        t=threading.Thread(target=self.backgroundThread,args=())    
        t.start()
        
    def start(self):
        self.locker.acquire()
        if self.runStatus==True:
            return
        else:
            self.runStatus=True
            self.startTask() #return immedialy
        self.locker.release()
        
    def stop(self):
        self.locker.acquire()
        if self.runStatus==False:
            return
        else:
            self.runStatus=False
        self.locker.release()
'''      
redisSettings={'redisHostname':'127.0.0.1','redisPort':6379,'redisDb':0}
@singleton
class WebSiteStatusService(object):
    def __init__(self,redisSettings=redisSettings):
        self.redisHostname=redisSettings['redisHostname']
        self.redisPort=redisSettings['redisPort']
        self.redisDb=redisSettings['redisDb']
    def displaySettings(self):
        print 'hostname:%s' %(self.redisHostname)
        
if __name__=='__main__':
    pass