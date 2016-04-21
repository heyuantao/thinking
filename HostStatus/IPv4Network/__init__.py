#install the package using pip install netaddr
from netaddr import IPNetwork
from Ping import Ping

class IPv4Network(object): 
    #only accept 24bit mask network address
    def __init__(self,subnet): 
        self.subnet=subnet
        self.networkObject=IPNetwork(subnet)
        if self.__isValid() is False:
            raise Exception('IPv4Network parameter error !')
        
    def __isValid(self):
        if self.networkObject.prefixlen!=24:
            return False
        else:
            return True
     
    def getIpList(self):
        ipList=[str(ip) for ip in self.networkObject]
        return ipList
    
    def getPingStatusOfNetwork(self):
        ping=Ping()
        ipList=[str(ip) for ip in self.networkObject]
        ping.setIpList(ipList)
        ping.checkIpStatus()
        ipStatusList=ping.getStatusList()
        return ipStatusList
        
    
    