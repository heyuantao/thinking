import redis
import time
import threading
import gevent
from netaddr import IPNetwork
from NetworkHostInformation import NetworkHostInformation

db='localhost'
#global settings
globalSettingsDict={'checkInterval':1,'redisHost':db,'redisPort':6379,'redisDb':0}

class HostCheckService(object):
    def __init__(self,settingsDict=globalSettingsDict):
        self.checkInterval=settingsDict['checkInterval']
        self.redisHost=settingsDict['redisHost']
        self.redisPort=settingsDict['redisPort']
        self.redisDb=settingsDict['redisDb']
        #check condition
        if self.checkInterval<=1:
            raise Exception("check interval time below than one !")
        
        #begin create the database and start the thread
        self.redisConnection=redis.Redis(host=self.redisHost,port=self.redisPort,db=self.redisDb)
        
        mainThread=threading.Thread(target=self.mainThreadLoop,args=())
        timestampThread=threading.Thread(targes=self.updateTimestampAndKeepAliveStatusInThread,args=())
        mainThread.daemon=True
        timestampThread.daemon=True
        mainThread.start()
        timestampThread.start()
        
    def start(self):
        self.redisConnection.set('STATUS','RUN')
        
    def stop(self):
        self.redisConnection.set('STATUS','STOP')
       
    def addNetwork(self,network):
        self.networkObject=IPNetwork(self.networkAddress)
        if self.networkObject.prefixlen!=24:
            return
        self.redisConnection.sadd('NETWORKS',network)
    def rmNetwork(self,network):
        self.networkObject=IPNetwork(self.networkAddress)
        if self.networkObject.prefixlen!=24:
            return
        self.redisConnection.srem('NETWORKS',network)
    def __needCheck(self):
        runStatus=self.redisConnection.get('STATUS')
        if runStatus is None:
            return False
        if runStatus=='RUN':
            return True
        if runStatus=='STOP':
            return False
    #def checkNetworksIn   
    def updateTimestampAndKeepAliveStatusInThread(self):
        while True:
            runStatus=self.redisConnection.get('STATUS')
            if (runStatus=='STOP') or (runStatus is None): #check and do nothing
                pass
            elif runStatus=='RUN':
                self.redisConnection.set('TIMESTAMP',int(time.time()))
            #update the keep alive status,self.checkInterval is timeout time
            self.redisConnection.setex('KEEPALIVE','TRUE',self.checkInterval)
            time.sleep(self.checkInterval)
    def mainThreadLoop(self):#continue forever
        while True:
            if self.__needCheck()==False:
                gevents=[gevent.spawn(fetch, i) for i in range(10)]
                pass
            else:
                pass
            time.sleep(self.checkInterval)
    def hostCheckGevent(self,network):
        returnDict={}
        networkHostInformation=NetworkHostInformation(network)
        hostDict=networkHostInformation.getHostStatus()
        returnDict[network]=hostDict
        return returnDict
    
def unitTestForHostCheckService():
    hostCheckService=HostCheckService()    
    print 'start'
    hostCheckService.start()    
    time.sleep(10)
    print 'stop'
    hostCheckService.stop()
    time.sleep(10)
    
if __name__=='__main__':
    unitTestForHostCheckService()          