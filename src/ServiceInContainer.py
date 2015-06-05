import time
import os
import commands
SERVICE_NAME_LIST=['mysql']

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
        
if __name__=='__main__':
    mysqlServiceCtrl=ServiceController('apache2')
    print 'current status is: %s' %(mysqlServiceCtrl.getServiceStatus())