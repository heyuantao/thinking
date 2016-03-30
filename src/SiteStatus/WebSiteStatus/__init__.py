import requests
import thread
import threading
import time
import gevent

class WebSiteStatus(object):
    def __init__(self):
        self.siteUrlList=[]
        self.siteStatuList=[] 
        self.runStatus=False
        
    def addSiteUrl(self,urlString):
        self.siteUrlList.append(urlString)
        self.siteStatuList.append(False)
        
    def theTask(self,siteUrlList,siteStatuList,index): 
        siteStatuList[index]=self.checkOneUrl(siteUrlList[index])
          
    def checkAll(self):
        for index,oneUrl in enumerate(self.siteUrlList):
            self.siteStatuList[index]=False            
        listLength=len(self.siteUrlList)
        threads=[gevent.spawn(self.theTask,self.siteUrlList,self.siteStatuList,index) for index in xrange(listLength)]
        gevent.joinall(threads)   
        
    def getStatusList(self):
        return self.siteStatuList
    
    def displayAllStatus(self):
        for index,oneUrl in enumerate(self.siteUrlList):   
            print "Url:%s  Status:%s" %(self.siteUrlList[index],self.siteStatuList[index])   
    def checkOneUrl(self,url):
        ret=requests.get(url)
        if ret.status_code==200:
            return True #means this site is online
        else:
            return False #means this site is down



if __name__=='__main__':
    pass