import os
import time
from HostCheckService import HostCheckService

def unitTestForMain():
    hostCheckService=HostCheckService()    
    print 'start'
    hostCheckService.addNetwork('192.168.133.0/24') 
    hostCheckService.addNetwork('192.168.132.0/24') 
    time.sleep(50)
    print 'stop'
    hostCheckService.stop()
    time.sleep(5)
    
if __name__=='__main__':
    unitTestForMain()   
