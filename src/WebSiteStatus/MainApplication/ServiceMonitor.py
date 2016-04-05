import thread
import threading
import time
import redis
import requests
import time
import gevent
from redis_lock import RedisLock

globalRedisSettings={'redisHostname':'127.0.0.1','redisPort':6379,'redisDb':0,'prefixInRedis':'URL','checkInterval':1}

#design pattern begin        
def singleton(class_):
  instances = {}
  def getinstance(*args, **kwargs):
    if class_ not in instances:
        instances[class_] = class_(*args, **kwargs)
    return instances[class_]
  return getinstance
#design pattern end

@singleton
class ServiceMonitor(object):
    def __init__(self,redisSettings=globalRedisSettings):
        self.redisHostname=redisSettings['redisHostname']
        self.redisPort=redisSettings['redisPort']
        self.redisDb=redisSettings['redisDb']
        self.prefixInRedis=redisSettings['prefixInRedis']
        self.checkInterval=redisSettings['checkInterval']
        self.redisConnection=redis.Redis(host=self.redisHostname,port=self.redisPort,db=self.redisDb)
        self.lock=RedisLock(self.redisConnection,lock_key='LOCK:WebSiteStatusService')
    def __removePrefix(self,string):
        stringArray=string.split(':')
        newStringArray=stringArray[1:] #remove the first part this is URL
        newString=':'.join(newStringArray) #reassemble the left things
        return newString
    def getServiceStatus(self):
        #statusDict={}
        runStatus=self.redisConnection.get('STATUS')
        if (runStatus is None)or(runStatus=='STOP'):
            runStatus='stop'
        if runStatus=='RUN':
            runStatus='run'
        #statusDict['service_status']=runStatus
        return runStatus
    def __addOneUrl(self,oneUrl=None):
        if oneUrl is None:
            return        
        if not isinstance(oneUrl, str):
            return
        self.redisConnection.sadd('SITES',oneUrl)
    def addUrlList(self,urlList=[]):
        if not isinstance(urlList, list):
            return
        self.lock.acquire()
        for oneUrl in urlList:
            self.__addOneUrl(oneUrl)
        self.lock.release()        
    def __removeUrl(self,oneUrl):
        if oneUrl is None:
            return        
        if not isinstance(oneUrl, str):
            return
        self.redisConnection.srem('SITES',oneUrl)
    def removeUrlList(self,urlList=[]):
        if not isinstance(urlList, list):
            return
        self.lock.acquire()
        for oneUrl in urlList:
            self.__removeUrl(oneUrl)
        self.lock.release()
        
    def changeServiceToRun(self):
        statusDict={}
        self.redisConnection.set('STATUS', 'RUN')
        statusDict['status']='success'
        return statusDict
    def changeServiceToStop(self):
        statusDict={}
        self.redisConnection.set('STATUS', 'STOP')
        statusDict['status']='success'
        return statusDict
    def getUrlList(self):        
        urlListSet=self.redisConnection.smembers('SITES')
        urlList=[oneUrl for oneUrl in urlListSet] #change the set into list of python
        returnDict={}
        #print urlList
        returnDict['urls']=urlList
        return returnDict
    def getURLStatus(self):
        keyPattern=self.prefixInRedis+':*' #'URL:*'
        urlListWithPrefix=self.redisConnection.keys(pattern=keyPattern)
        urlList=[self.__removePrefix(item) for item in urlListWithPrefix ]
        statusList=[]
        for oneUrlWithPrefix in urlListWithPrefix:
            oneStatus=self.redisConnection.get(oneUrlWithPrefix)
            statusList.append(oneStatus)
        urlDict={}
        for url,status in zip(urlList,statusList):
            urlDict[url]=status
        returnDict={}
        returnDict['urls']=urlDict
        timeStamp=self.redisConnection.get('TIMESTAMP')
        if timeStamp is None:
            timeStamp=''
        returnDict['timestamp']=timeStamp
        return returnDict
        
        