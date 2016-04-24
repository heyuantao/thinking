import redis
import time
import threading
import gevent
import threading
from DesignPattern import singleton
from netaddr import IPNetwork
from NetworkHostInformation import NetworkHostInformation

db='localhost'
#global settings
globalSettingsDict={'checkInterval':20,'redisHost':db,'redisPort':6379,'redisDb':0}

#this object is used by django app
@singleton
class HostCheckServiceMonitor(object):
    def __init__(self,settingsDict=globalSettingsDict):
        self.checkInterval=settingsDict['checkInterval']
        self.redisHost=settingsDict['redisHost']
        self.redisPort=settingsDict['redisPort']
        self.redisDb=settingsDict['redisDb']
        #begin create the database and start the thread
        self.redisConnection=redis.Redis(host=self.redisHost,port=self.redisPort,db=self.redisDb)
        
    def isServiceProcessDown(self):
        keepaliveStatus=self.redisConnection.get('KEEPALIVE')        
        if keepaliveStatus=='TRUE':
            return False
        else:
            return True        
    def getServiceStatus(self):
        #statusDict={}
        runStatus=self.redisConnection.get('STATUS')
        if (runStatus is None)or(runStatus=='STOP'):
            runStatus='stop'
        if runStatus=='RUN':
            runStatus='run'
        #statusDict['service_status']=runStatus
        return runStatus    
    def changeServiceToRun(self):
        self.redisConnection.set('STATUS','RUN')
        
    def changeServiceToStop(self):
        self.redisConnection.set('STATUS','STOP')
        
    def addNetworkList(self,networkList):
        for oneNetwork in networkList:
            self.networkObject=IPNetwork(oneNetwork)
            if self.networkObject.prefixlen!=24:
                raise Exception("only support 24bit mask network type !")
            self.redisConnection.sadd('NETWORKS',oneNetwork)
            
    def removeNetworkList(self,networkList):
        for oneNetwork in networkList:
            self.networkObject=IPNetwork(oneNetwork)
            if self.networkObject.prefixlen!=24:
                return
            self.redisConnection.srem('NETWORKS',oneNetwork)
            
    def getNetworkList(self):
        networkListSet=self.redisConnection.smembers('NETWORKS')
        networkList=[oneNetwork for oneNetwork in networkListSet] #change the set into list of python
        returnDict={}
        #print urlList
        returnDict['networks']=networkList
        return returnDict
        
    def getNetworkStatus(self):  
        self.__clearNetworkNotInList()
        keyPattern="IP"+':*' #'URL:*'
        networkListWithPrefix=self.redisConnection.keys(pattern=keyPattern)
        networkList=[self.__removePrefix(item) for item in networkListWithPrefix ]
        statusList=[]
        for oneNetworkWithPrefix in networkListWithPrefix:
            oneNetworkStatus=self.redisConnection.get(oneNetworkWithPrefix)
            statusList.append(oneNetworkStatus)
        print statusList
        networkDict={}
        for network,status in zip(networkList,statusList):
            networkDict[network]=status
        returnDict={}
        returnDict['networks']=networkDict
        return returnDict
    def __clearNetworkNotInList(self):
        keyPattern="IP"+':*' #'URL:*'
        networkListWithPrefix=self.redisConnection.keys(pattern=keyPattern)
        networkList=[self.__removePrefix(item) for item in networkListWithPrefix ]  
        
        networkListSet=self.redisConnection.smembers('NETWORKS')
        networkListToBeCheck=[network for network in networkListSet]
        
        for oneNetwork in networkList:
            if not oneNetwork in networkListToBeCheck:
                self.redisConnection.delete('IP:'+oneNetwork)
        
    def __removePrefix(self,string):
        stringArray=string.split(':')
        newStringArray=stringArray[1:] #remove the first part this is URL
        newString=':'.join(newStringArray) #reassemble the left things
        return newString
    
    
#this object is use by backgroud deamon
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
            raise Exception("only support 24bit mask network type !")
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
            networkList=self.redisConnection.smembers('NETWORKS')
            if (self.__needCheck()==True) and( len(networkList)>0 ):                
                threadList=[threading.Thread(target=self.hostCheckTask, args=(oneNetwork,)) for oneNetwork in networkList]
                
                [thread.start() for thread in threadList]
                [thread.join() for thread in threadList]
                #update the timestamp after every check
                self.redisConnection.set('TIMESTAMP',int(time.time()))
                
            time.sleep(self.checkInterval)
    def hostCheckTask(self,network):
        #returnDict={}
        networkHostInformation=NetworkHostInformation(network)
        hostDict=networkHostInformation.getHostStatus()
        #returnDict[network]=hostDict
        #print 'check',network
        networkTag="IP:"+network
        self.redisConnection[networkTag]=hostDict
    
        