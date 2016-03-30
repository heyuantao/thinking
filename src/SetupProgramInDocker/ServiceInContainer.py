import time
import os
import sys
import commands
#this is a smart tools for docker , to setup a system service on start
#in this case,we setup mysql and apache to begin
SERVICE_LIST=['apache2','mysql']

class ServiceController(object):
    STOP_KEYWORDS=['not running','stop','waiting']
    RUN_KEYWORDS=['running','start']
    RC_ROOT='/etc/init.d/'
    def __init__(self,service): #service is a string of service
        self.service=service
        self.startCmd='service '+service+' start'
        self.stopCmd='service '+service+' stop'
        self.statusCmd='service '+service+' status'
    def getServiceStatus(self):
        (status,output)=commands.getstatusoutput(self.statusCmd)
        if status==0: #the command was excude successfull
            output=output.lower()
            for word in self.STOP_KEYWORDS:
                if word in output:
                    return False
            for word in self.RUN_KEYWORDS:
                if word in output:
                    return True
        else:
            return False
    def isServiceExist(self):
        filePath=os.path.join(self.RC_ROOT,self.service)
        if os.path.exists(filePath):
            return True
        else:
            return False
    def startService(self):
        (status,output)=commands.getstatusoutput(self.startCmd)
    def stopService(self):
        (status,output)=commands.getstatusoutput(self.stopCmd)

class ToolForDocker(object):
    @classmethod
    def waitForEver(cls):
        sleepTimeInSecond=60*60 #sleep for a hour
        time.sleep(sleepTimeInSecond)
        
if __name__=='__main__':
    #
    ServiceCtrlList=[]
    for item in SERVICE_LIST:
        serviceInstance=ServiceController(item)
        ServiceCtrlList.append(serviceInstance)
    
    statusList=[x.isServiceExist() for x in ServiceCtrlList]
    if statusList.count(False)>0:
        print 'A Service does not exist !'
        sys.exit(-1)
        
    for x in ServiceCtrlList:
        if not x.getServiceStatus(): #if the service not up
            x.startService()
    print 'Finish Start The Service'
    #ToolForDocker.waitForEver() #enter the loop and does not exist
    '''    
    mysqlServiceCtrl=ServiceController('mysql')
    apacheServiceCtrl=ServiceController('apache2')
    if mysqlServiceCtrl.isServiceExist() and apacheServiceCtrl.isServiceExist():
        if mysqlServiceCtrl.getServiceStatus()==False:
            mysqlServiceCtrl.startService()
        if apacheServiceCtrl.getServiceStatus()==False:
            apacheServiceCtrl.startService()
    print 'Finish Start The Service'
    ToolForDocker.waitForEver() #enter the loop and does not exist
    '''