from redis import StrictRedis

cache = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
