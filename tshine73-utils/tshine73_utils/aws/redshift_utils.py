import psycopg2


def query(sql, conn):
    cur = execute(sql, conn)
    records = cur.fetchall()
    return records


def update(sql, conn):
    cur = execute(sql, conn)
    return cur.rowcount


def execute(sql, conn):
    cur = conn.cursor()
    cur.execute(sql)

    return cur


def get_connection(dbname, host, port, user, password):
    conn = psycopg2.connect(
        dbname=dbname,
        host=host,
        port=port,
        user=user,
        password=password
    )

    return conn
