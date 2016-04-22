import pyping
import multiprocessing


class Ping(object):
    def __init__(self,hostList):
        self.hostList=[]
        self.hostStatusList=[]
        self.hostAverageRTT=[]
        #check the param type
        if not type(self.hostList) is list:
            raise Exception('host list is not list !')
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

    def checkOneHostStatusTask(self,queue,lock,host):
        r = pyping.ping(host) 
        retDic={}
        retDic['ip']=host
        if r.ret_code==0:            
            retDic['online']=True
            retDic['avg_rtt']=float(r.avg_rtt)
        else:
            retDic['online']=False
            retDic['avg_rtt']=float(-1)
        lock.acquire()
        queue.put(retDic)
        lock.release()

    def checkIpStatusInThread(self):
        queue = multiprocessing.Queue(1000)
        lock=multiprocessing.Lock()
        processList=[multiprocessing.Process(target=self.checkOneHostStatusTask,args=(queue,lock,oneHost,)) for oneHost in self.hostList]
        
        for oneProcess in processList:
            oneProcess.start()
        for oneProcess in processList:
            oneProcess.join()
        
        while not queue.empty():
            one=queue.get()
            self.hostList.append(one['ip'])
            self.hostStatusList.append(one['online'])
            self.hostAverageRTT.append(one['avg_rtt'])
            
            
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