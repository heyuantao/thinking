import nmap
import multiprocessing


class Nmap(object):
    def __init__(self,hostList):
        self.hostList=[]
        self.hostStatusList=[]
        self.hostAverageRTT=[]
        #check the param type
        if not type(self.hostList) is list:
            raise Exception('host list is not list !')
        else:
            self.hostList=hostList
    

if __name__=='__main__':
    print 'hello'