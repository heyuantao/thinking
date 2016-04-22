import nmap

class NetworkHostInformation(object):
    def __init__(self,networkAddress):
        self.networkAddress=networkAddress
    def getHostStatus(self):
        nm = nmap.PortScanner()
        nm.scan(hosts=self.networkAddress, arguments='-n -sP -PE')
        self.hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
        return self.hosts_list

if __name__=='__main__':
    networkHostInformation=NetworkHostInformation('192.168.37.0/24')
    print networkHostInformation.getHostStatus()
    