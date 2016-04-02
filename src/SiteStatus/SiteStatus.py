from WebSiteStatus import WebSiteStatus
from WebSiteStatusService import WebSiteStatusService
import time

if __name__=='__main__':
    service=WebSiteStatusService()
    list=['http://www.sina.com.cn','http://www.baidu.com','http://www.zol.com.cn']
    newList=['http://202.196.166.180']
    service.addUrlList(list)
    service.displayContent()
    service.startService()
    time.sleep(5)
    service.addUrlList(newList)
    time.sleep(5)
    service.removeUrlList(newList)
    time.sleep(25)
    service.stopService()