import requests
import json

DEBUG=True

def debugMessage(msg):
    if DEBUG is True:
        print msg
    else:
        pass
    
class BandwagonHost(object):
    def __init__(self,id,key):
        self.id=id
        self.key=key
    def __getHostStatus(self):
        requestUrl=self.__generateAccessUrl()
        httpRequest=requests.get(requestUrl)
        self.hostBasicInformationJson=httpRequest.content.encode("utf-8")
    def getBasicInformation(self):
        requestUrl = "https://api.64clouds.com/v1/getServiceInfo?veid=%s&api_key=%sE" %(self.id,self.key)
        httpRequest=requests.get(requestUrl)
        return httpRequest.content.encode("utf-8")
    def getServiceInformation(self):
        requestUrl = "https://api.64clouds.com/v1/getLiveServiceInfo?veid=%s&api_key=%sE" %(self.id,self.key)
        httpRequest=requests.get(requestUrl)
        return httpRequest.content.encode("utf-8")   
    def getAvailableOS(self):
        requestUrl = "https://api.64clouds.com/v1/getAvailableOS?veid=%s&api_key=%sE" %(self.id,self.key)
        httpRequest=requests.get(requestUrl)
        return httpRequest.content.encode("utf-8")  
    def rebootOS(self):
        requestUrl = "https://api.64clouds.com/v1/restart?veid=%s&api_key=%sE" %(self.id,self.key)
        httpRequest=requests.get(requestUrl)
        return httpRequest.content.encode("utf-8")  
    def stopOS(self):
        requestUrl = "https://api.64clouds.com/v1/stop?veid=%s&api_key=%sE" %(self.id,self.key)
        httpRequest=requests.get(requestUrl)
        return httpRequest.content.encode("utf-8")  
    def startOS(self):
        requestUrl = "https://api.64clouds.com/v1/start?veid=%s&api_key=%sE" %(self.id,self.key)
        httpRequest=requests.get(requestUrl)
        return httpRequest.content.encode("utf-8")  