import socket
import threading
import netaddr
#from netaddr import IPNetwork

class HostCheck(object):
    def __init__(self,host,portList):
        self.host=host
        self.portList=portList
        self.portStatusList=[False for oneport in self.portList]
    def isThisPortOpen(self,index,portList,portStatusList): 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((self.host,portList[index]))
        if result == 0:
           portStatusList[index]=True
        else:
           portStatusList[index]=False
           
    def isHostUp(self):
        threadList=[]        
        for index in range(len(self.portList)):
            oneThread=threading.Thread(target=self.isThisPortOpen,args=(index,self.portList,self.portStatusList))
            threadList.append(oneThread)
        [oneThread.start() for oneThread in threadList]
        [oneThread.join() for oneThread in threadList]
        #print self.portStatusList
        finalStatus=False
        for status in self.portStatusList:
            finalStatus=finalStatus or status
        #print finalStatus
        
class NetStatus(object):
    def __init__(self,ipList):
        self.ipList=ipList
        self.ipStatusList=[False for item in self.ipList]
        #oneNetObject=netaddr.IPNetwork(self.oneNet)
        #if oneNetObject.prefixlen!=24:
        #    raise Exception("network address format error !")
    def netStatus(self):
        pass
        
if __name__=='__main__':
    portList=[80,23,441,133,53]
    hostCheck=HostCheck('127.0.0.1',portList)
    hostCheck.isHostUp()