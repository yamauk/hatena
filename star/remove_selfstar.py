import redis
if __name__ == '__main__':
    red = redis.Redis(host='127.0.0.1', port=6379, db=0)
    keys=red.keys('*')
    for key in keys:
        val=red.hgetall(key)
        if key in val:
            print key,val[key],val
            del val[key]
            if len(val)!=0:
                red.hdel(key,key)
            else:
                red.delete(key)