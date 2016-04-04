import thread
import threading
import time
import redis
import requests
import time
import gevent
from redis_lock import RedisLock

globalRedisSettings={'redisHostname':'127.0.0.1','redisPort':6379,'redisDb':0,'prefixInRedis':'URL'}

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
        self.lock=RedisLock(self.redisConnection,lock_key='LOCK:WebSiteStatusService')
    def __addOneUrl(self,oneUrl=None):
        if oneUrl is None:
            return        
        #print type(oneUrl)
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
        #self.lock.acquire()
        self.redisConnection.srem('SITES',oneUrl)
        #self.lock.release()
    def removeUrlList(self,urlList=[]):
        if not isinstance(urlList, list):
            return
        self.lock.acquire()
        for oneUrl in urlList:
            self.__removeUrl(oneUrl)
        self.lock.release()
    def __removePrefix(self,string):
        stringArray=string.split(':')
        newStringArray=stringArray[1:] #remove the first part this is URL
        newString=':'.join(newStringArray) #reassemble the left things
        return newString
    def startService(self):
        needReRun=False
        self.lock.acquire()
        runStatus=self.redisConnection.get('STATUS')
        if (runStatus=='STOP')or(runStatus is None):
            self.redisConnection.set('STATUS','RUN')
            needReRun=True
        else: #already run
            needReRun=False
        self.lock.release()
        
        if needReRun==True:
            tMain=threading.Thread(target=self.runServiceInThread,args=())    
            tSlave=threading.Thread(target=self.updateTimestampInThread,args=()) 
            tMain.start()
            tSlave.start()
            
    def updateTimestampInThread(self):
        while True:
            runStatus=self.redisConnection.get('STATUS')
            if runStatus=='STOP':
                print 'no timestamp'
                time.sleep(1)
                continue
            self.redisConnection.set('TIMESTAMP',int(time.time()))
            print 'timestamp'
            time.sleep(1)
            
    def runServiceInThread(self):
        while True: #this thread will loop forever
            runStatus=self.redisConnection.get('STATUS')
            if runStatus=='STOP':
                print 'no check'
                time.sleep(1)
                continue
            print 'check'
            webSiteStatus=WebSiteStatus()
            for oneUrl in self.redisConnection.smembers('SITES'):
                webSiteStatus.addSiteUrl(oneUrl)
            webSiteStatus.checkAll()
            (urlList,stateList)=webSiteStatus.getStatusList()
            
            #append the site state into redis
            for oneUrl,oneState in zip(urlList,stateList):
                key='URL:'+oneUrl
                self.redisConnection.set(key,oneState)
                
            #remove the url not in urlList
            keyPattern=self.prefixInRedis+':*' #'URL:*'
            oldUrlListWithPrefix=self.redisConnection.keys(pattern=keyPattern)
            oldUrlList=[self.__removePrefix(item) for item in oldUrlListWithPrefix ]
            newUrlList=self.redisConnection.smembers('SITES')
            
            self.lock.acquire()
            for oneUrl in oldUrlList:
                if oneUrl not in  newUrlList:
                    self.redisConnection.delete(self.prefixInRedis+':'+oneUrl)
            self.lock.release()
            
            #print 'checking !'                       
            #webSiteStatus.displayAllStatus()
            #self.redisConnection.set('TIMESTAMP',int(time.time()))
            time.sleep(1)
        #self.redisConnection.set('STATUS','STOP')  
    def stopService(self):
        self.lock.acquire()
        if self.redisConnection.get('STATUS')=='RUN':
            self.redisConnection.set('STATUS','STOP')
        else:
            pass
        self.lock.release()
    def getStatus(self):
        returnStr=""
        returnStr+= 'HOST:%s PORT:%s DB:%s' %(self.redisHostname,self.redisPort,self.redisDb)
        returnStr+= 'SITE LIST:%s' %(self.redisConnection.smembers('SITES'))
        returnStr+= 'This is the content of begin'
        return returnStr
    def getUrlList(self):
        urlList=[]
        listSet=self.redisConnection.smembers('SITES')
        for item in listSet:
            urlList.append(item)
        return urlList
class WebSiteStatus(object):
    def __init__(self):
        self.siteUrlList=[]
        self.siteStatuList=[] 
        self.runStatus=False
        
    def addSiteUrl(self,urlString):
        self.siteUrlList.append(urlString)
        self.siteStatuList.append(False)
        
    def theTask(self,siteUrlList,siteStatuList,index): 
        siteStatuList[index]=self.checkOneUrl(siteUrlList[index])
          
    def checkAll(self):
        for index,oneUrl in enumerate(self.siteUrlList):
            self.siteStatuList[index]=False            
        listLength=len(self.siteUrlList)
        threads=[gevent.spawn(self.theTask,self.siteUrlList,self.siteStatuList,index) for index in xrange(listLength)]
        gevent.joinall(threads)   
        
    def getStatusList(self):
        return (self.siteUrlList,self.siteStatuList)
    
    def displayAllStatus(self):
        for index,oneUrl in enumerate(self.siteUrlList):   
            print "Url:%s  Status:%s" %(self.siteUrlList[index],self.siteStatuList[index])   
    def checkOneUrl(self,url):
        ret=requests.get(url)
        if ret.status_code==200:
            return True #means this site is online
        else:
            return False #means this site is down

        
if __name__=='__main__':
    pass