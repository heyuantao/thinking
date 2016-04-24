from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from HostCheckService import HostCheckServiceMonitor
import urls
# Create your views here.
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
        hostCheckServiceMonitor=HostCheckServiceMonitor()
        serverStatusDict={}
        if hostCheckServiceMonitor.isServiceProcessDown():
            serverStatusDict['server_status']='down'
            serverStatusDict['support_status']=self.supportStatus
            return Response(serverStatusDict)
        #otherwise the service is in run or stop status
        else:
            serverStatus=hostCheckServiceMonitor.getServiceStatus()        
            serverStatusDict['server_status']=serverStatus
            serverStatusDict['support_status']=self.supportStatus
        return Response(serverStatusDict)
    def post(self,request):
        dictData=request.data
        newStatus=dictData['server_status'].encode('utf-8')
        
        hostCheckServiceMonitor=HostCheckServiceMonitor()
        if newStatus=='run':
            print 'run'
            hostCheckServiceMonitor.changeServiceToRun()
            return Response(successStatus)
        elif newStatus=='stop':
            print 'stop'
            hostCheckServiceMonitor.changeServiceToStop()
            return Response(successStatus)
        else:
            print 'unsupport command'
            return Response(rejectStatus,status=status.HTTP_403_FORBIDDEN)
        
#  {"networks":["192.168.1.0/24","192.168.2.0/24"]} 
class AddNetwork(APIView):
    def get(self,request):
        return Response(successStatus)
    def post(self,request):
        dictData=request.data
        urlListWithUnicode=dictData['networks']
        urlList=[oneUrl.encode('utf-8') for oneUrl in urlListWithUnicode]
        print urlList
        serviceMonitor=HostCheckServiceMonitor()
        serviceMonitor.addNetworkList(urlList)
        return Response(successStatus)
#  {"networks":["192.168.1.0/24","192.168.2.0/24"]} 
class RemoveNetwork(APIView):
    def get(self,request):
        return Response(successStatus)
    def post(self,request):
        dictData=request.data
        urlListWithUnicode=dictData['networks']
        urlList=[oneUrl.encode('utf-8') for oneUrl in urlListWithUnicode]
        print urlList
        serviceMonitor=HostCheckServiceMonitor()
        serviceMonitor.removeNetworkList(urlList)
        return Response(successStatus)

class NetworkList(APIView):
    #renderer_classes = (JSONRenderer, )
    def get(self,request):
        serviceMonitor=HostCheckServiceMonitor()
        urlDict=serviceMonitor.getNetworkList()
        return Response(urlDict)
    def post(self,request):
        return Response(successStatus)
    
#{"status":"start"}
class NetworkStatus(APIView):
    def get(self,request):
        serviceMonitor=HostCheckServiceMonitor()
        statusDict=serviceMonitor.getNetworkStatus()    
        #print statusDict    
        return Response(statusDict)
    def post(self,request):    
        return Response(successStatus)