import redis
from rq import Worker, Queue, Connection

redis_conn = redis.Redis(host='localhost', port=6379, db=0)

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(['default'], connection=redis_conn)
        worker.work()