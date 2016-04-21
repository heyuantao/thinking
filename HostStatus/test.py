from IPv4Network  import  IPv4Network
import os

if __name__=="__main__":
    ipv4Network=IPv4Network('192.168.20.0/24')
    print ipv4Network.getIpList()
    print ipv4Network.getPingStatusOfNetwork()
    #print iPv4Network.isValid()
    #net=IPNetwork('10.0.2.0/24')
    #print net.netmask ,net.broadcast
    #print net.prefixlen
    #ipList=list(net)
    #for item in ipList:
    #    print str(item)
