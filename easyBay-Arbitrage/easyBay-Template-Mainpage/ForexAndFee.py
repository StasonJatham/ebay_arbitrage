import requests 
import json 
import SQLite_util



def get_forex(conn_forex, currency):
    sql = ("SELECT value FROM forex WHERE currency = \"{0}\"".format(currency))
    cur = conn_forex.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    try:
        return rows[0][0]
    except:
        print(rows)



class ForexAndFee():

    def exchange_rate(_to, _amount):
        forex_db = "C:\\Users\\karlm\\Google Drive\\Coding\\easyBay-Arbitrage\\forex.db"
        SQLite_util.make_db(forex_db)
        conn_forex = SQLite_util.create_connection(forex_db)

        with conn_forex:
            if conn_forex is not None:
                exchange_rate = get_forex(conn_forex, _to)
                exchange_rate = float(_amount) / float(exchange_rate)
                
            return exchange_rate


    def paypal_fee(item_price,currency="EUR",selling=False):
        """
        INPUT: 
            item_price, currency, selling
            item_price -> eBay Item 
            currency   -> EUR or PLN or GBP ..whatever
            selling    -> True or False 
        Output:
            {currency : paypal_fee} -> "EUR" : 5.02
        """
        # gebühr für geldempfang
        #(2,49% + 0,35 EUR)
        # + wechselkurs wenn nicht euro 
        # -----------------------------------------------------------------------------------------
        # Albanien, Andorra, Belarus, Bosnien und Herzegowina, Bulgarien, Georgien, 
        # Kosovo, Kroatien, Lettland, Liechtenstein, Litauen, Mazedonien, Polen, Republik Moldau, 
        # Rumänien, Russland, Schweiz, Serbien, Tschechische Republik, Ukraine, Ungarn 
        # 3% gebühr auf vollen Preis bei NICHT Euro EU Ländern
        
        if selling:
            paypal_fee = float(item_price) * 0.0249 + 0.35
            if currency != "EUR":
                paypal_fee = paypal_fee + (paypal_fee*0.03) 

        if selling == False:
            paypal_fee = 0
            if currency != "EUR":
                paypal_fee = paypal_fee + (float(item_price)*0.03)

        dict_paypal = {currency : paypal_fee}

        return dict_paypal 


    def ebay_fee(item_price, currency="EUR"):
        #Die Verkaufsprovision beträgt einheitlich 10 % des Verkaufspreises ohne Verpackung und Versand (max. 199,00 Euro). 
        seller_fee = float(item_price) * 0.1

        if seller_fee > 199.00:
            seller_fee = 199.00

        dict_seller = {currency : seller_fee}

        return dict_seller


    def amazon_fee(item_price, currency="EUR"):
        # Actually not correct since computer 7%, handy 10% and electronics 15%
        # varies greatly with category, for now we use base of 15%
        seller_fee = float(item_price) * 0.15
        dict_seller = {currency : seller_fee}
        return dict_seller


# ---> Usage for exchange_rate
#print(ForexAndFee.exchange_rate("PLN",100))

# ---> Usage for paypal fee 
# Forex.paypal_fee(100,"EUR",True)