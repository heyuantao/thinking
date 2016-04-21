import pyping
import gevent

class Ping(object):
    def __init__(self):
        self.hostList=[]
        self.hostStatusList=[]
        self.hostAverageRTT=[]
    def setIpList(self,hostList):
        if not type(self.hostList) is list:
            return
        else:
            self.hostList=hostList
    def checkIpStatus(self):
        if len(self.hostList)==0:
            self.hostStatusList=[]
        else:
            return self.checkIpStatusInThread()
    def getStatusList(self):
        if len(self.hostList)!=len(self.hostStatusList):
            return []
        else:
            return self.hostStatusList
    def getAverageRTTList(self):
        if len(self.hostList)!=len(self.hostAverageRTT):
            return []
        else:
            return self.hostAverageRTT        
    def checkOneHostStatusTask(self,host):
        print 'ping',host
        r = pyping.ping(host) 
        if r.ret_code==0:
            return (True,float(r.avg_rtt))
        else:
            return (False,float(-1))
    def checkIpStatusInThread(self):
        threads=[gevent.spawn(self.checkOneHostStatusTask,oneHost) for oneHost in self.hostList]
        gevent.joinall(threads)
        self.hostStatusList=[oneThread.value[0] for oneThread in threads]
        self.hostAverageRTT=[oneThread.value[1] for oneThread in threads]
        
'''
def unitTest():
    addList=['www.sina.com.cn','www.baidu.com','202.196.166.180','202.196.166.181']
    pingService=Ping()       
    pingService.setIpList(addList)
    print 'begin check'
    pingService.checkIpStatus()
    print 'check end'
    print pingService.getStatusList()
    print pingService.getAverageRTTList()
    for item in pingService.getAverageRTTList():
        print type(item)        
if __name__=='__main__':
    pass
    #unitTest()
    '''