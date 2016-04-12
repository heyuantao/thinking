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
            return self.checkIpStatusInThread()
    def getStatusList(self):
        if len(self.ipAddressList)!=len(self.ipStatusList):
            return []
        else:
            return self.ipStatusList
    def checkOneIpStatusTask(self,host):
        r = pyping.ping(host) 
        if r.ret_code==0:
            return True
        else:
            return False
    def checkIpStatusInThread(self):
        threads=[gevent.spawn(self.checkOneIpStatusTask,oneAddress) for oneAddress in self.ipAddressList]
        gevent.joinall(threads)
        self.ipStatusList=[oneThread.value for oneThread in threads]
        
        
if __name__=='__main__':
    addList=['www.sina.com.cn','www.baidu.com','202.196.166.180','202.196.166.181']
    pingService=PingService()       
    pingService.setIpList(addList)
    print 'begin check'
    pingService.checkIpStatus()
    print 'check end'
    print pingService.getStatusList()