import socket
import threading
import netaddr
#from netaddr import IPNetwork

class HostCheck(object):
    def __init__(self,sock,host,portList):
        self.sock=sock
        self.host=host
        self.portList=portList
        self.portStatusList=[False for oneport in self.portList]
    def isThisPortOpen(self,port): 
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = self.sock.connect_ex((self.host,port))
        if result == 0:
           return True
        else:
           return False
           
    def isHostUp(self):
        threadList=[]     
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        for index in range(len(self.portList)):
            self.portStatusList[index]=self.isThisPortOpen(self.portList[index])
        finalStatus=False
        for status in self.portStatusList:
            finalStatus=finalStatus or status
        #sock.close()
        return finalStatus
        
class NetStatus(object):
    def __init__(self,ipList):
        self.ipList=ipList
        self.ipStatusList=[False for item in self.ipList]
        self.portCheckList=[22,80,443]
        #oneNetObject=netaddr.IPNetwork(self.oneNet)
        #if oneNetObject.prefixlen!=24:
        #    raise Exception("network address format error !")
    def isOneHostUp(self,sock,oneHost):
        hostCheck=HostCheck(sock,oneHost,self.portCheckList)
        return hostCheck.isHostUp()
    def status(self):    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for index in range(len(self.ipList)):            
            self.ipStatusList[index]=self.isOneHostUp(sock,self.ipList[index])
        finalStatus=False
        for status in self.ipStatusList:
            finalStatus=finalStatus or status     
        sock.close()
        return self.ipStatusList
        #print self.ipStatusList   
if __name__=='__main__':
    #portList=[80,23,441,133,53]
    #hostCheck=HostCheck('127.0.0.1',portList)
    #hostCheck.isHostUp()
    oneNetObject=netaddr.IPNetwork('192.168.10.1/24')
    hostObjectList=list(oneNetObject)
    hostList=[str(hostObject) for hostObject in hostObjectList]
    hostList.remove(str(oneNetObject.network))
    hostList.remove(str(oneNetObject.broadcast))
    print hostList
    ipList=hostList
    #ipList=['192.168.10.1', '192.168.10.2', '192.168.10.3', '192.168.10.4', '192.168.10.5', '192.168.10.6', '192.168.10.7', '192.168.10.8', '192.168.10.9', '192.168.10.10', '192.168.10.11', '192.168.10.12', '192.168.10.13', '192.168.10.14', '192.168.10.15', '192.168.10.16', '192.168.10.17', '192.168.10.18']
    #netStatus=NetStatus(ipList[:100])
    #netStatus.status()
    #print "next"
    netStatus2=NetStatus(ipList)
    
    
    print netStatus2.status()
    print len(ipList)