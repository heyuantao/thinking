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
    def __init__(self):
        self.hostIdKeyName="hostId"
        self.hostSecretKeyName="hostSecret"
    def get(self,request):
        format={"id":"","secret":""}
        return Response(format)
    def post(self,request):
        dictData=request.data
        #print dictData
        try:
            hostIdValue=dictData['id'].encode('utf-8')
            hostSecretValue=dictData['secret'].encode('utf-8')
        except Exception :            
            return Response(rejectStatus)
        
        idobj,created=KeyValueStorage.objects.get_or_create(key=self.hostIdKeyName)
        idobj.value=hostIdValue
        idobj.save()
        secobj,created=KeyValueStorage.objects.get_or_create(key=self.hostSecretKeyName)
        secobj.value=hostSecretValue
        secobj.save()
        
        return Response(successStatus)
        