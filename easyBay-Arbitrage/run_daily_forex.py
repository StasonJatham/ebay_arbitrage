"""
RUN THIS SCRIPT ONCE EVERY DAY
 - 7 AM 
 - 7 DAYS A WEEK
"""


import requests 
import json 
import SQLite_util
from Get_api_key import Get_api_key


def insert_forex(conn_key, currency_value_date):
    sql = ('INSERT INTO forex(currency, value, date) VALUES(?,?,?)')
    cur = conn_key.cursor()
    cur.execute(sql, currency_value_date)
    conn_key.commit()
    return cur.lastrowid

def get_forex(conn_forex, currency):
    sql = ("SELECT value FROM forex WHERE currency = \"{0}\"".format(currency))
    cur = conn_forex.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    try:
        return rows[0][0]
    except:
        print(rows)


fixer_key = Get_api_key.fixer_key()


forex_db = "C:\\Users\\karlm\\Google Drive\\Coding\\easyBay-Arbitrage\\forex.db"
SQLite_util.make_db(forex_db)
conn_forex = SQLite_util.create_connection(forex_db)

sql_create_forex_table = """ CREATE TABLE IF NOT EXISTS forex (
                                    id integer PRIMARY KEY,
                                    currency text NOT NULL,
                                    value text NOT NULL,
                                    date text NOT NULL
                                ); """

currency_list = ["PLN","GBP","USD"]
_from = "EUR"
for _to in currency_list:
    with conn_forex:
        if conn_forex is not None:
            SQLite_util.create_table(conn_forex, sql_create_forex_table)
            """
            INPUT:
                _from, _to , _amount
                Example: "EUR","PLN",100
            OUT:
                {'success': True, 'timestamp': 1559025485, 'base': 'EUR', 'date': '2019-05-28', 'rates': {'PLN': 4.291863}, 'amount': 429.1863}
            """
            exchange= requests.get("http://data.fixer.io/api/latest?access_key={0}&base={1}&symbols={2}".format(fixer_key,_from,_to))
            exchange_json = json.loads(exchange.text)

            currency_value_date = (_to,str(exchange_json["rates"][_to]),exchange_json["date"])

            try:
                check_forex_update(conn_forex, currency_value_date)
            except:
                insert_forex(conn_forex, currency_value_date)

            print(get_forex(conn_forex, _to))


