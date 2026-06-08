import psycopg2

CONNECTION_STRING = "postgresql://carquery_db_user:kLylUkzDSjoibsUCJOkJH97V2YCDu2Rj@dpg-d8i7dsuk1jcs739va1s0-a.virginia-postgres.render.com/carquery_db"

_connection = None

def get_connection():
    global _connection
    if _connection is None or _connection.closed:
        _connection = psycopg2.connect(CONNECTION_STRING)
    return _connection

def close_connection():
    global _connection
    if _connection and not _connection.closed:
        _connection.close()
        _connection = None