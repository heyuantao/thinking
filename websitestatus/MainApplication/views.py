from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import urls

from MainApplication.ServiceMonitor import ServiceMonitor

successStatus={"status":"success"}
rejectStatus={"status":"reject"}

# Create your views here.
class IndexPage(APIView):
    def get(self,request):
        pathDict={}
        pathList=[]
        for item in urls.urlpatterns:
            print item.regex.pattern
            pathList.append(item.regex.pattern)
        pathDict['paths']=pathList
        return Response(pathDict)
    
class ServiceStatus(APIView):
    def __init__(self):
        self.supportStatus=['run','stop']
    def get(self,request):
        serviceMonitor=ServiceMonitor()
        serverStatusDict={}
        if serviceMonitor.isServiceProcessDown():
            serverStatusDict['server_status']='down'
            serverStatusDict['support_status']=self.supportStatus
            return Response(serverStatusDict)
        #otherwise the service is in run or stop status
        else:
            serverStatus=serviceMonitor.getServiceStatus()        
            serverStatusDict['server_status']=serverStatus
            serverStatusDict['support_status']=self.supportStatus
        return Response(serverStatusDict)
    def post(self,request):
        dictData=request.data
        newStatus=dictData['server_status'].encode('utf-8')
        
        serviceMonitor=ServiceMonitor()
        if newStatus=='run':
            print 'run'
            serviceMonitor.changeServiceToRun()
            return Response(successStatus)
        elif newStatus=='stop':
            print 'stop'
            serviceMonitor.changeServiceToStop()
            return Response(successStatus)
        else:
            print 'unsupport command'
            return Response(rejectStatus,status=status.HTTP_403_FORBIDDEN)
#  {"urls":["www.sina.com.cn","www.baidu.com"]}     
class AddUrl(APIView):
    def get(self,request):
        return Response(successStatus)
    def post(self,request):
        dictData=request.data
        urlListWithUnicode=dictData['urls']
        urlList=[oneUrl.encode('utf-8') for oneUrl in urlListWithUnicode]
        print urlList
        serviceMonitor=ServiceMonitor()
        serviceMonitor.addUrlList(urlList)
        return Response(successStatus)
#  {"urls":["http://www.sina.com.cn","http://www.zol.com.cn"]}    
class RemoveUrl(APIView):
    def get(self,request):
        return Response(successStatus)
    def post(self,request):
        dictData=request.data
        urlListWithUnicode=dictData['urls']
        urlList=[oneUrl.encode('utf-8') for oneUrl in urlListWithUnicode]
        print urlList
        serviceMonitor=ServiceMonitor()
        serviceMonitor.removeUrlList(urlList)
        return Response(successStatus)
    
class UrlList(APIView):
    #renderer_classes = (JSONRenderer, )
    def get(self,request):
        serviceMonitor=ServiceMonitor()
        urlDict=serviceMonitor.getUrlList()
        return Response(urlDict)
    def post(self,request):
        return Response(successStatus)
#{"status":"start"}
class SiteStatus(APIView):
    def get(self,request):
        serviceMonitor=ServiceMonitor()
        statusDict=serviceMonitor.getURLStatus()        
        return Response(statusDict)
    def post(self,request):    
        return Response(successStatus)
        
