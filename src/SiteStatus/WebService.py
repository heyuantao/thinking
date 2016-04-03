from flask import Flask
from WebSiteStatusService import WebSiteStatusService

application = Flask(__name__)

@application.route('/')
def hello():
    return "This is the service for detect web site status !"

@application.route('/status')
def status():
    webSiteStatusService=WebSiteStatusService()
    str=webSiteStatusService.getStatus()
    return str

@application.route('/addurl/<oneUrl>')
def addUrl(oneUrl):
    urlList=[]
    urlList.append(oneUrl.encode('utf-8'))
    webSiteStatusService=WebSiteStatusService()
    print urlList
    str=webSiteStatusService.addUrlList(urlList)
    return 'add success'

@application.route('/urllist/')
def urlList():
    webSiteStatusService=WebSiteStatusService()
    list=webSiteStatusService.getUrlList()
    print list
    listStr=','.join(list)
    return listStr

if __name__ == "__main__":
    application.run(host='0.0.0.0')
