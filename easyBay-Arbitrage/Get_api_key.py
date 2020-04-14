import SQLite_util

key_db   = "C:\\Users\\karlm\\Google Drive\\Coding\\easyBay-Arbitrage\\key.db"
SQLite_util.make_db(key_db)
conn_key   = SQLite_util.create_connection(key_db)

def insert_key(conn_key, name_key):
    sql = ('INSERT INTO api(name, key) VALUES(?,?)')
    cur = conn_key.cursor()
    cur.execute(sql, name_key)
    conn_key.commit()
    return cur.lastrowid

def get_key(conn_key, name_col):
    sql = ("SELECT key FROM api WHERE name = \"{0}\"".format(name_col))
    cur = conn_key.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows[0][0]


class Get_api_key():

    def ebay_key():
        return get_key(conn_key,"ebay_app_id")

    def fixer_key():
        return get_key(conn_key,"fixer")