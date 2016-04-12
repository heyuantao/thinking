import pyping
import gevent

class PingService(object):
    def __init__(self):
        self.ipAddressList=[]
        self.ipStatusList=[]
    def setIpList(self,ipAddressList):
        if not type(self.ipAddressList) is list:
            return
        else:
            self.ipAddressList=ipAddressList
    def checkIpStatus(self):
        if len(self.ipAddressList)==0:
            self.ipStatusList=[]
        else:
            return self.checkIpStatusInThread(self.ipAddressList)
    def getStatusList(self):
        if len(self.ipAddressList)!=len(self.ipStatusList):
            return []
        else:
            return self.ipStatusList
    def checkOneIpStatus(self,):
    def checkIpStatusInThread(self,ipAddressList):
        thread=[]
        for i in range(0:len(ipAddressList)):
            thread.append(gevent.)
        
        