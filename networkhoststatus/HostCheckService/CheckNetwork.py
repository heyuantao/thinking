import socket
import threading
import netaddr
import nmap
from DesignPattern import singleton

GlobalPortCheckList=[22,53,80,443,445]   
#62078 is iphone-sync service

class HostCheck(object):
    def __init__(self,host,portList):
        self.host=host
        self.portList=portList
        self.portStatusList=[False for oneport in self.portList]
    def isThisPortOpen(self,port): 
        #print 'check:',self.host,"port:",port
        self.sock.settimeout(0.1)
        result = self.sock.connect_ex((self.host,port))  
        if result == 0:
           return True
        else:
           return False               
    def isHostUp(self): #check which port is open,return the open port ,otherwise return -1
        threadList=[]     
        #first check the custom port list
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        for index in range(len(self.portList)):
            onePortStatus=self.isThisPortOpen(self.portList[index])
            if onePortStatus==True:    
                #print 'last open port check'            
                self.sock.close()
                return self.portList[index]
        #then check the global port list without the last check port
        globalPortList=[oneport for oneport in GlobalPortCheckList]
        for onePortToRemove in self.portList:
            if onePortToRemove in globalPortList:
                globalPortList.remove(onePortToRemove)
        for index in range(len(globalPortList)):
            onePortStatus=self.isThisPortOpen(globalPortList[index])
            if onePortStatus==True:
                #print 'list port check'
                self.sock.close()
                return globalPortList[index]
        #none of port in list is open,so do a full check
        fullServerPortList=[onePort for onePort in range(1,1024)]
        for onePortToRemove in GlobalPortCheckList:
            if onePortToRemove in fullServerPortList:
                fullServerPortList.remove(onePortToRemove)
        for onePortToRemove in self.portList:
            if onePortToRemove in fullServerPortList:        
                fullServerPortList.remove(onePortToRemove)
        #print 'full port check'
        for index in range(len(fullServerPortList)):
            onePortStatus=self.isThisPortOpen(fullServerPortList[index])
            if onePortStatus==True:
                self.sock.close()
                return fullServerPortList[index]
        #if none of port is open,the ip may not be used
        self.sock.close()
        return -1
    
#Container and implement of OneNetStatus
GlobalOneNetStatus={}    #store the one network information     
class OneNetStatus(object):
    def __new__(cls, *args, **kwargs):
        try:
            if args[0] is None:
                raise Exception('Args is null !')
            for key,object in GlobalOneNetStatus.items():
                if key==args[0]:
                    #print 'get old'
                    return object
            #print 'create new'
            newObj=super(OneNetStatus,cls).__new__(cls)
            GlobalOneNetStatus[args[0]]=newObj
            return newObj
        except Exception:
            raise "Create OneNetStatus Error !"        
    def __init__(self,oneNetwork):
        self.oneNetwork=oneNetwork
        self.ipList=self.__getIpListFromOneNet(oneNetwork)
        if hasattr(self, "ipStatusList"):
            pass
        else:
            self.ipStatusList=[-1 for item in self.ipList]
    def oneOpenPortInHost(self,oneHost):
        portCheckList=[]
        lastOpenPort=self.lastCheckPort(oneHost)
        if lastOpenPort>0:
            #print 'use last check port:',lastOpenPort
            portCheckList.append(lastOpenPort)
        hostCheck=HostCheck(oneHost,portCheckList)
        openedPort=hostCheck.isHostUp()
        #print 'Host:',oneHost,'port:',openedPort
        return openedPort
    #return the last check opened port
    def lastCheckPort(self,ip):
        index=self.ipList.index(ip)
        return self.ipStatusList[index]
    def checkStatus(self):    
        #check tcp port by connect it
        for index in range(len(self.ipList)):            
            self.ipStatusList[index]=self.oneOpenPortInHost(self.ipList[index])
        #check the icmp
        nm = nmap.PortScanner()
        nm.scan(hosts=self.oneNetwork, arguments='-n -sP -PE')
        hostStatusList=[]
        for x in nm.all_hosts():
            index=self.ipList.index(x)
            if self.ipStatusList[index]>0:
                pass
            else:
                self.ipStatusList[index]=0
        #return hostStatusList
    def getIpList(self):
        return self.ipList
    def getIpStatusList(self):
        return self.ipStatusList
    def getStatus(self):
        return [{'ip':oneIp,'port':onePort} for oneIp,onePort in zip(self.ipList,self.ipStatusList)]
    def __getIpListFromOneNet(self,oneNetwork):
        oneNetObject=netaddr.IPNetwork(oneNetwork)
        hostObjectList=list(oneNetObject)
        hostList=[str(hostObject) for hostObject in hostObjectList]
        hostList.remove(str(oneNetObject.network))
        hostList.remove(str(oneNetObject.broadcast))
        return hostList
    def __isCClassNetwork(self,oneNet):
        networkObject=netaddr.IPNetwork(oneNet)
        if networkObject.prefixlen!=24:
            return False
        else:
            return True
 
@singleton       
class NetworkStatus(object):
    def __init__(self):
        self.networkList=[]
        
    def addOneNet(self,oneNet):
        if self.__isCClassNetwork(oneNet):    
            if oneNet in self.networkList:
                pass
            else:   
                self.networkList.append(oneNet)
        else:
            raise Exception("Network is not type C !")
    def removeOneNet(self,oneNet):
        if oneNet in self.networkList:
            self.networkList.remove(oneNet)
        else:
            pass
    def getNetworkList(self):
        return self.networkList
    def checkOneNetInThread(self,networkList,networkStatusList,index):
        network=networkList[index]
        oneNetStatus=OneNetStatus(network)
        oneNetStatus.checkStatus()
        networkStatusList[index]=oneNetStatus.getStatus()
    def checkAllNet(self): #check every net in thread
        self.networkStatusList=[None for item in self.networkList]
        threadList=[threading.Thread(target=self.checkOneNetInThread,args=(self.networkList,self.networkStatusList,index)) for index in range(len(self.networkList))]
        [oneThread.start() for oneThread in threadList]
        [oneThread.join() for oneThread in threadList]
    def getNetworkStatus(self,oneNet):
        try:
            oneNetStatus=OneNetStatus(oneNet)
            return oneNetStatus.getStatus()
        except Exception:
            return []
    def getAllStatus(self):
        returnDict=[]
        for oneNet in self.networkList:
            oneItem={}
            oneItem[oneNet]=OneNetStatus(oneNet).getStatus()
            returnDict.append(oneItem)
        return returnDict
    def __isCClassNetwork(self,oneNet):
        networkObject=netaddr.IPNetwork(oneNet)
        if networkObject.prefixlen!=24:
            return False
        else:
            return True

'''
if __name__=='__main__':
    networkStatus=NetworkStatus()
    networkStatus.addOneNet('192.168.10.1/24')
    networkStatus.addOneNet('192.168.0.1/24')
    #networkStatus.checkAllNet()
    print networkStatus.getNetworkStatus('192.168.0.1/24')
'''