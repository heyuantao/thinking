import thread
import threading
import time
import redis
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
globalRedisSettings={'redisHostname':'127.0.0.1','redisPort':6379,'redisDb':0,'prefixInRedis':'URL'}
@singleton
class WebSiteStatusService(object):
    #add queue name is 'SITEADDQUEUE'
    #rm queue name is 'SITERMQUEUE'
    #current queue name is 'SITECURRENTQUEUE'
    def __init__(self,redisSettings=globalRedisSettings):
        self.redisHostname=redisSettings['redisHostname']
        self.redisPort=redisSettings['redisPort']
        self.redisDb=redisSettings['redisDb']
        self.prefixInRedis=redisSettings['prefixInRedis']
        self.redisConnection=redis.Redis(host=self.redisHostname,port=self.redisPort,db=self.redisDb)
    def addOneUrl(self,oneUrl=None):
        if oneUrl is None:
            return        
        if not isinstance(oneUrl, str):
            return
        #keyString=self.prefixInRedis+":"+oneUrl
        #self.redisConnection.hset(keyString, 'status',' check')
        self.redisConnection.sadd('SITEADDQUEUE',oneUrl)
    def addUrlList(self,urlList=[]):
        if not isinstance(urlList, list):
            return
        for oneUrl in urlList:
            self.addOneUrl(oneUrl)
    def removeUrl(self,oneUrl):
        if oneUrl is None:
            return        
        if not isinstance(oneUrl, str):
            return
        self.redisConnection.sadd('SITERMQUEUE',oneUrl)
    def removeUrlList(self,urlList=[]):
        if not isinstance(urlList, list):
            return
        for oneUrl in urlList:
            self.removeUrl(oneUrl)
    def __removePrefix(self,string):
        stringArray=string.split(':')
        newStringArray=stringArray[1:] #remove the first part this is URL
        newString=':'.join(newStringArray) #reassemble the left things
        return newString
    def displayContent(self):
        print 'HOST:%s PORT:%s DB:%s' %(self.redisHostname,self.redisPort,self.redisDb)
        print 'Queue for add:%s' %(self.redisConnection.smembers('SITEADDQUEUE'))
        print 'Queue for remove:%s' %(self.redisConnection.smembers('SITERMQUEUE'))
        print 'This is the content of begin'
        prefixPattern=self.prefixInRedis+'*'
        for key in self.redisConnection.keys(pattern=prefixPattern):
            newKey=self.__removePrefix(key)
            print '%s' %(newKey)
        print 'This is the content of end'
        
if __name__=='__main__':
    pass