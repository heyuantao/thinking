from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import urls
import json
from BandwagonHostService import BandwagonHostService
from hostinformation.models import KeyValueStorage
from utils import SystemSettings


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
        hostId=SystemSettings.getHostId()
        hostSecret=SystemSettings.getHostSecret()
        print hostId,hostSecret
        #the hostId and hostSecret my be empty because it was not set
        if ((hostId=="") or (hostSecret=="")):
            return Response(rejectStatus)
        
        statusDict={}
        bandwagonHostService=BandwagonHostService(id=hostId,key=hostSecret)
        #print bandwagonHostService.getBasicInformation()
        statusDict['basic_information']=json.loads(bandwagonHostService.getBasicInformation())
        statusDict['service_information']=json.loads(bandwagonHostService.getServiceInformation())
        
        return Response(statusDict)
    def post(self,request):
        dictData=request.data
        return Response(rejectStatus,status=status.HTTP_403_FORBIDDEN)

class HostSetting(APIView):
    def get(self,request):
        format={"id":"","secret":""}
        return Response(format)
    def post(self,request):
        dictData=request.data
        #print dictData
        try:
            hostIdValue=dictData['id'].encode('utf-8')
            hostSecretValue=dictData['secret'].encode('utf-8')        
            # save the data to database
            SystemSettings.setHostId(hostIdValue)
            SystemSettings.setHostSecret(hostSecretValue)
        except Exception :            
            return Response(rejectStatus)
        return Response(successStatus)
        