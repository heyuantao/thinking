from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import urls

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

class AddOneChannel(APIView):    
	def get(self,request):
		pass 
       
