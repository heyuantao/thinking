# This program is used for host discovery
#nm = nmap.PortScanner()
#nm.scan(hosts=self.networkAddress, arguments='-n -sP -PE')
#self.hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]

import nmap
from netaddr import IPNetwork

class NetworkHostInformation(object):
    def __init__(self,networkAddress):
        self.networkAddress=networkAddress
        networkObject=IPNetwork(self.networkAddress)
        if networkObject.prefixlen!=24:
            raise Exception("network address format error !")
        
    def getHostStatus(self):
        nm = nmap.PortScanner()
        nm.scan(hosts=self.networkAddress, arguments='-n -sP -PE')
        hostStatusDic={}
        #self.hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
        for x in nm.all_hosts():
            hostStatusDic[x]=nm[x]['status']['state']
        return hostStatusDic

if __name__=='__main__':
    #networkHostInformation=NetworkHostInformation('202.196.166.1/24')
    #print networkHostInformation.getHostStatus()
    networkHostInformation=NetworkHostInformation('192.168.130.0/24')
    print networkHostInformation.getHostStatus()
    