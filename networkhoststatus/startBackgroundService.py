from HostCheckService import HostCheckService
import time
#start of program
if __name__=='__main__':
    hostCheckService=HostCheckService()
    hostCheckService.start()
    hostCheckService.addNetwork('192.168.1.1/24')
    while True:
        time.sleep(10)
        