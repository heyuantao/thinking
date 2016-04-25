from HostCheckService import HostCheckService
import time
#start of program
if __name__=='__main__':
    hostCheckService=HostCheckService()
    hostCheckService.start()
    while True:
        time.sleep(10)
        