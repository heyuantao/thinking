from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import urls
from BandwagonHostService import BandwagonHostService
from hostinformation.models import KeyValueStorage

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
    
class HostStatus(APIView):
    def get(self,request):
        '''
        BandwagonHostService=BandwagonHostService()
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
        '''
        return Response(successStatus)
    def post(self,request):
        dictData=request.data
        return Response(rejectStatus,status=status.HTTP_403_FORBIDDEN)

class HostSetting(APIView):
    def get(self,request):
        return Response(successStatus)
    def post(self,request):
        dictData=request.data
        try:
            hostId=dictData['id'].encode('utf-8')
            hostKey=dictData['key'].encode('utf-8')
            oneKeyValue=KeyValueStorage(key=hostId,value=hostKey)
            oneKeyValue.save()
        except Exception:            
            return Response(rejectStatus)