import pyping
import multiprocessing
def checkOneHostStatusTask(queue,lock,host):
    r = pyping.ping(host) 
    retDic={}
    if r.ret_code==0:    
        retDic['ip']=host
        retDic['online']=True
        retDic['avg_rtt']=float(r.avg_rtt)
    else:
        retDic['ip']=host
        retDic['online']=False
        retDic['avg_rtt']=float(-1)
    lock.acquire()
    queue.put(retDic)
    lock.release()

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

    def checkIpStatusInThread(self):
        queue = multiprocessing.Queue(600)
        lock=multiprocessing.Lock()
        for oneHost in self.hostList:
            print oneHost
        processList=[multiprocessing.Process(target=checkOneHostStatusTask,args=(queue,lock,oneHost)) for oneHost in self.hostList]
        for process in processList:
            process.start()
        for process in processList:
            process.join()
        while not queue.empty():
            print queue.get()['ip'],queue.get()['online']
        '''
    def checkIpStatusInThread(self):
        threads=[gevent.spawn(self.checkOneHostStatusTask,oneHost) for oneHost in self.hostList]
        gevent.joinall(threads)
        self.hostStatusList=[oneThread.value[0] for oneThread in threads]
        self.hostAverageRTT=[oneThread.value[1] for oneThread in threads]
        '''
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