import pymysql

def get_conn():
    conn = pymysql.connect(
        host = "", #endpoint link
        port = 3306,
        user = "",
        password = "",
        db = "",
    )
    return conn
