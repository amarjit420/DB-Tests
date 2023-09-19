#!/usr/bin/env python3

# step 1 - import the redis-py client package
import redis

# step 2 - define our connection information for Redis
# Replaces with your configuration information
redis_host = "localhost"
redis_port = 6379
redis_password = ""


def hello_world():
    """Example Hello World Program"""

    # step 3 - create the Redis Connection object
    try:

        # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
        # using the default encoding utf-8.  This is client specific.
      
        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

        # step 4 - Set the hello message in Redis
        r.set("msg:greeting", "Hello World!")

        # step 5 - Retrieve the message 
        msg = r.get("msg:greeting")
        print(msg)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    hello_world()
