import socket
import threading
import netaddr
#from netaddr import IPNetwork
   
class HostCheck(object):
    def __init__(self,host,portList):
        self.host=host
        self.portList=portList
        self.portStatusList=[False for oneport in self.portList]
    def isThisPortOpen(self,port): 
        #print 'check:',self.host,"port:",port
        self.sock.settimeout(0.2)
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
                print 'without full check'
                self.sock.close()
                return self.portList[index]
        #none of port in list is open,so do a full check
        fullServerPortList=[onePort for onePort in range(1,1024)]
        [fullServerPortList.remove(onePortToRemove) for onePortToRemove in self.portList]
        print 'do full check'
        for index in range(len(fullServerPortList)):
            onePortStatus=self.isThisPortOpen(fullServerPortList[index])
            if onePortStatus==True:
                self.sock.close()
                return fullServerPortList[index]
        #if none of port is open,the ip may not be used
        self.sock.close()
        return -1
        
class NetStatus(object):
    def __init__(self,ipList):
        self.ipList=ipList
        self.ipStatusList=[-1 for item in self.ipList]
        self.portCheckList=[22,53,80,443,445]
    def oneOpenPortInHost(self,oneHost):
        hostCheck=HostCheck(oneHost,self.portCheckList)
        openedPort=hostCheck.isHostUp()
        return openedPort
    def status(self):    
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for index in range(len(self.ipList)):            
            self.ipStatusList[index]=self.oneOpenPortInHost(self.ipList[index])
        finalStatus=False
        for status in self.ipStatusList:
            finalStatus=finalStatus or status     
        #sock.close()
        return self.ipStatusList
        #print self.ipStatusList   
if __name__=='__main__':
    oneNetObject=netaddr.IPNetwork('202.196.166.180/24')
    #oneNetObject=netaddr.IPNetwork('192.168.20.1/24')
    hostObjectList=list(oneNetObject)
    hostList=[str(hostObject) for hostObject in hostObjectList]
    hostList.remove(str(oneNetObject.network))
    hostList.remove(str(oneNetObject.broadcast))
    ipList=hostList
    netStatus2=NetStatus(ipList)
    
    
    print netStatus2.status()
    #print len(ipList)