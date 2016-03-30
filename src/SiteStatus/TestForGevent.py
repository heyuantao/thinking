import grequests
import time

if __name__=='__main__':
    start_time = time.time()
    urls = [
        "http://202.196.166.180/",
        "http://202.196.166.180/downloads/",
        "http://202.196.166.180/exps/course/",
        "http://202.196.166.180/bysj/Account",
        "http://202.196.166.180/cxxf/UserLogin",
        "http://202.196.166.180/JudgeOnline/",
        "http://202.196.166.180/owncloud/",
        "http://202.196.166.181/heyuantao/",
        "http://www.hudieshanfood.com/"
    ]
    
    rs = (grequests.get(u) for u in urls)
    result=grequests.map(rs)
    
    
    for item in result:
        if item is None:
            print "None"
            continue
        else:
            print item.status_code

    print("--- %s seconds ---" % (time.time() - start_time))