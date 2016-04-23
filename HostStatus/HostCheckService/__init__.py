import redis
import time
import threading
import gevent
import threading
from netaddr import IPNetwork
from NetworkHostInformation import NetworkHostInformation

db='localhost'
#global settings
globalSettingsDict={'checkInterval':5,'redisHost':db,'redisPort':6379,'redisDb':0}

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
        timestampThread=threading.Thread(target=self.updateKeepAliveStatusInThread,args=())
        mainThread.daemon=True
        timestampThread.daemon=True
        mainThread.start()
        timestampThread.start()
        
    def start(self):
        self.redisConnection.set('STATUS','RUN')
        
    def stop(self):
        self.redisConnection.set('STATUS','STOP')
       
    def addNetwork(self,network):
        self.networkObject=IPNetwork(network)
        if self.networkObject.prefixlen!=24:
            return
        self.redisConnection.sadd('NETWORKS',network)
    def rmNetwork(self,network):
        self.networkObject=IPNetwork(network)
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
    def updateKeepAliveStatusInThread(self):
        while True:
            #runStatus=self.redisConnection.get('STATUS')
            #if (runStatus=='STOP') or (runStatus is None): #check and do nothing
            #    pass
            #elif runStatus=='RUN':
            #    pass
            #update the keep alive status,self.checkInterval is timeout time
            self.redisConnection.setex('KEEPALIVE','TRUE',int(self.checkInterval)-1)
            time.sleep(int(self.checkInterval)-1)
    def mainThreadLoop(self):#continue forever
        while True:
            if self.__needCheck()==False:
                networkList=self.redisConnection.smembers('NETWORKS')
                #gevents=[gevent.spawn(self.hostCheckGevent, oneNetwork) for oneNetwork in networkList]
                threadList=[threading.Thread(target=self.hostCheckTask, args=(oneNetwork,)) for oneNetwork in networkList]
                #print 'create gevents'
                [thread.start() for thread in threadList]
                [thread.join() for thread in threadList]
                #update the timestamp after every check
                self.redisConnection.set('TIMESTAMP',int(time.time()))
            else:
                pass            
            time.sleep(self.checkInterval)
    def hostCheckTask(self,network):
        #returnDict={}
        networkHostInformation=NetworkHostInformation(network)
        hostDict=networkHostInformation.getHostStatus()
        #returnDict[network]=hostDict
        print 'check',network
        self.redisConnection[network]=hostDict
    
        