import redis

if __name__=='__main__':
    redisConnection=redis.Redis(host='localhost',port=6379,db=0)
    redisConnection.set('address','xingyang')
    #info=redisConnection.info()
    #print info
    keyList=redisConnection.keys(pattern='*')
    for key in keyList:
        print "Key:%s Value:%s" %(key,redisConnection.get(key))