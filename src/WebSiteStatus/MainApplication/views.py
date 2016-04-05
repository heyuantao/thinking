from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import subprocess
import os
import tools
from MainApplication.ServiceMonitor import ServiceMonitor

successStatus={"status":"success"}
rejectStatus={"status":"reject"}

# Create your views here.
class ServiceStatus(APIView):
    def get(self,request):
        currentStatus={'status':'stoped'}
        return Response(currentStatus)
    def post(self,request):
        dictData=request.data
        newStatus=dictData['status'].encode('utf-8')
        if newStatus=='start':
            print 'start service'
            tools.runScriptInBackground()
            return Response(successStatus)
        elif newStatus=='stop':
            print 'stop service'
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
#  {"urls":["www.sina.com.cn","www.zol.com.cn"]}    
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
        