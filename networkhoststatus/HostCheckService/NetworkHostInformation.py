# This program is used for host discovery
#nm = nmap.PortScanner()
#nm.scan(hosts=self.networkAddress, arguments='-n -sP -PE')
#self.hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]

import nmap
from netaddr import IPNetwork

class NetworkHostInformation(object):
    def __init__(self,networkAddress):
        self.networkAddress=networkAddress
        self.networkObject=IPNetwork(self.networkAddress)
        if self.networkObject.prefixlen!=24:
            raise Exception("network address format error !")
        
    def getHostStatus(self):
        nm = nmap.PortScanner()
        nm.scan(hosts=self.networkAddress, arguments='-n -sP -PE')
        print 'check finished !'
        hostStatusDic={}
        #self.hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
        for x in nm.all_hosts():
            if self.networkObject.network==x:
                #print 'network'
                continue
            if self.networkObject.broadcast==x:
                #print 'boardcast'
                continue
            hostStatusDic[x]=nm[x]['status']['state']
        return hostStatusDic


    