import psycopg2.pool
from env import DB_NAME, DB_USER, DB_HOST, DB_PORT, DB_PASS

connection_pool = None


def create_pool():
    global connection_pool
    if not connection_pool:
        connection_pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=1, maxconn=10,
            dbname=DB_NAME, user=DB_USER,
            password=DB_PASS, host=DB_HOST, port=DB_PORT)


def get_connection():
    global connection_pool
    if not connection_pool:
        create_pool()
    return connection_pool.getconn()


def put_connection(connection):
    global connection_pool
    connection_pool.putconn(connection)





