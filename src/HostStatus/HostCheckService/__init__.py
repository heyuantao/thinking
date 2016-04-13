import redis
import time
import threading

db='localhost'
#global settings
globalSettingsDict={'checkInterval':2,'redisHost':db,'redisPort':6379,'redisDb':0}

class HostCheckService(object):
    def __init__(self,settingsDict=globalSettingsDict):
        self.checkInterval=settingsDict['checkInterval']
        self.redisHost=settingsDict['redisHost']
        self.redisPort=settingsDict['redisPort']
        self.redisDb=settingsDict['redisDb']
        self.redisConnection=redis.Redis(host=self.redisHost,port=self.redisPort,db=self.redisDb)
        
        mainThread=threading.Thread(target=self.mainThreadLoop,args=())
        mainThread.daemon=True
        mainThread.start()
        
    def start(self):
        self.redisConnection.set('STATUS','RUN')
        
    def stop(self):
        self.redisConnection.set('STATUS','STOP')
        
    def __needCheck(self):
        runStatus=self.redisConnection.get('STATUS')
        if runStatus is None:
            return False
        if runStatus=='RUN':
            return True
        if runStatus=='STOP':
            return False
        
    def mainThreadLoop(self):#continue forever
        while True:
            if self.__needCheck()==False:
                print 'not check'
            else:
                print 'check'
            time.sleep(self.checkInterval)

def unitTest():
    print 'main'
    hostCheckService=HostCheckService()    
    print 'start'
    hostCheckService.start()    
    time.sleep(10)
    print 'stop'
    hostCheckService.stop()
    time.sleep(10)
    
if __name__=='__main__':
    unitTest()          