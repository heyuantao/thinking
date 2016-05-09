from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from models import ChannelModel
from modelsSerializer import ChannelModelSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import urls
from django.http.response import HttpResponse


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


class ChannelList(APIView):
    def get(self, request):
        serializer=ChannelModelSerializer(ChannelModel.objects.all(), many=True)
        return Response(serializer.data)
    def post(self,request):
        #print request.data
        #data = JSONParser().parse(request)
        #data={"description":"502","url":"rstp.ok"}
        serializer = ChannelModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)
    
class ChannelDetail(APIView):
    def get(self,request,pk,format=None):
        try:
            oneChannel=ChannelModel.objects.get(pk=pk)
            serializer=ChannelModelSerializer(oneChannel)
            return Response(serializer.data)  
        except ChannelModel.DoesNotExist:
            return HttpResponse(status=404)      
    def put(self,request,pk):        
        try:
            oneChannel=ChannelModel.objects.get(pk=pk)
            data = JSONParser().parse(request)
            serializer = ChannelModelSerializer(oneChannel, data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ChannelModel.DoesNotExist:
            return HttpResponse(status=404)     
    def delete(self,request,pk):
        try:
            oneChannel=ChannelModel.objects.get(pk=pk)
            oneChannel.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ChannelModel.DoesNotExist:
            return HttpResponse(status=404)             
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)