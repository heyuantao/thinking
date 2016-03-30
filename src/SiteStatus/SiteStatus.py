from WebSiteStatus import WebSiteStatus
from WebSiteStatusService import WebSiteStatusService
import time

if __name__=='__main__':
    '''
    start_time = time.time()
    
    otherSiteStatus=WebSiteStatus()
    otherSiteStatus.addSiteUrl("http://www.sina.com.cn")
    otherSiteStatus.addSiteUrl("http://www.baidu.com/oswe1")
    otherSiteStatus.checkAll()
    otherSiteStatus.displayAllStatus()
    
    print("--- %s seconds ---" % (time.time() - start_time))
    '''
    #urlList=['http://www.sina.com.cn','http://www.baidu.com/']
    service=WebSiteStatusService()
    list=['http://www.sina.com.cn','http://www.baidu.com']
    service.addOneUrl('http://www.zol.com.cn')
    service.addUrlList(list)
    service.removeUrlList(list)
    service.displayContent()
    #service.setUrlList(urlList)
    #service.start()
    #time.sleep(10)
    #service.addUrlList('http://202.196.166.180')
    #time.sleep(100)
    #service.stop()