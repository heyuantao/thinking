from HostCheckService import HostCheckService
import time
#start of program
if __name__=='__main__':
    hostCheckService=HostCheckService()
    hostCheckService.start()
    hostCheckService.addNetwork('192.168.133.1/24')
    time.sleep(50)
    #while True:
    #    time.sleep(10)
        