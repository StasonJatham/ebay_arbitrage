import requests
from bs4 import BeautifulSoup
import time 
from fake_useragent import UserAgent
import SQLite_util
import ebaysdk
from ebaysdk.finding import Connection as finding
import json 
from ForexAndFee import ForexAndFee
from Get_api_key import Get_api_key
from ebaysdk.merchandising import Connection as merchandising
from ebaysdk.exception import ConnectionError
from ebaysdk.shopping import Connection as Shopping


def random_header():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    return(headers)


class Cheapest():
    def __init__(self,title,location,price,picture):
        self.title  = title 
        self.location = location
        self.price = price 
        self.picture = picture 


class Expensive():
    def __init__(self,title,location,price,picture):
        self.title = title 
        self.location = location 
        self.price = price 
        self.picture = picture


class Profit():
    def __init__(self,raw_profit,paypal_fee,ebay_fee,real_profit):
        self.raw_profit  = raw_profit
        self.paypal_fee  = paypal_fee
        self.ebay_fee    = ebay_fee
        self.real_profit = real_profit




class Ebay():
    KARL_ID = Get_api_key.ebay_key()

    def get_trends():
        database = "C:\\Users\\karlm\\Google Drive\\Coding\\easyBay-Arbitrage\\easyBay-Template-Mainpage\\all_deal.db"
        conn = SQLite_util.create_connection(database)

        sql_create_ebay_trends_table = """ CREATE TABLE IF NOT EXISTS ebay_trends (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL
                                        ); """

        SQLite_util.create_table(conn, sql_create_ebay_trends_table)


        #returns a list of all ebay trends from .com .uk and .de
        list_all_items = []
        all_ebay_trending = ["https://www.ebay.de/trending/",
                            "https://www.ebay.com/trending/",
                            "https://www.ebay.co.uk/trending/"
                            ]
        for trend in all_ebay_trending:
            response = requests.get(trend, headers=random_header())
            soup = BeautifulSoup(response.text, 'html.parser')
            time.sleep(2)
            trending_items = soup.select('div > div > div > h2')
            for item in trending_items:
                list_all_items.append(item.a.contents[0])

        for item_name in list_all_items:
            cur = conn.cursor()
            cur.execute('INSERT INTO ebay_trends VALUES (NULL,\"{}\")'.format(str(item_name)))
            conn.commit()
        conn.close()

        return list_all_items


    def find_related_searches(searchword):
        api = Shopping(appid=Ebay.KARL_ID, config_file=None)

        mySearch = {
            "MaxKeywords": 10,
            "QueryKeywords": searchword,
        }
        api.execute('FindPopularSearches', mySearch)
        
        return(api.response_json())

            
    def get_top_watched_items(country_id):
        try:
            api = merchandising(siteid=country_id,appid=Ebay.KARL_ID,config_file=None, warnings=True)
            api.execute('getMostWatchedItems', {  
                'maxResults': 10,
            })

            return api.response_json()

        except ConnectionError as e:
            print(e)
            print(e.response.dict())


    def country_request(ebay_country,app_id,item):
        country_short = str(ebay_country).split("-")[1]

        try:
            api = finding(siteid='{0}'.format(ebay_country), appid=app_id, config_file=None)

            # https://developer.ebay.com/devzone/finding/CallRef/findItemsAdvanced.html#Request.itemFilter
            api.execute('findItemsAdvanced', {
                'keywords': '{0}'.format(item),
                'categoryId': '9355', # --> you only get trash results without a category
                'itemFilter': [ 
                    # itemFilter.name -> https://developer.ebay.com/devzone/finding/CallRef/types/ItemFilterType.html
                    {'name': 'Condition', 'value': '1000'},
                    {'name': 'LocatedIn', 'value': '{0}'.format(country_short)},
                    {'name': 'ListingType', 'value': 'FixedPrice'},
                    {'name': 'AvailableTo', 'value':'DE'},
                    {'name': 'FeedbackScoreMin', 'value':1},
                    {'name': 'MinPrice', 'value':10},
                    {'name': 'PaymentMethod', 'value':'PayPal'},
                ],
                #"outputSelector": "AspectHistogram", # --> gets more defined filters for this type of product
                'paginationInput': { 'entriesPerPage': '20', 'pageNumber': '1'},
                #'sortOrder': 'PricePlusShippingLowest'
                'sortOrder': 'BestMatch'
            })

            print("=====================================================================================")
            print(api.response_json())
            print("=====================================================================================")
            return api.response_json()

        except ConnectionError as e:
            print(e)


    # Usage: Ebay.get_all_countries_for_item("Microsoft Surface Go 128GB")
    def get_all_countries_for_item(search_word):


        category_id_list = """
            Antiques #20081
            Art #550
            Baby #2984
            Books #267
            Business & Industrial #12576
            Cameras & Photo #625
            Cell Phones & Accessories #15032
            Clothing, Shoes & Accessories #11450
            Coins & Paper Money #11116
            Collectibles #1
            Computers/Tablets & Networking #58058
            Consumer Electronics #293
            Crafts #14339
            Dolls & Bears #237
            DVDs & Movies #11232
            Entertainment Memorabilia #45100
            Everything Else #99
            Gift Cards & Coupons #172008
            Health & Beauty #26395
            Home & Garden #11700
            Jewelry & Watches #281
            Music #11233
            Musical Instruments & Gear #619
            Pet Supplies #1281
            Pottery & Glass #870
            Real Estate #10542
            Specialty Services #316
            Sporting Goods #888
            Sports Mem, Cards & Fan Shop #64482
            Stamps #260
            Tickets & Experiences #1305
            Toys & Hobbies #220
            Travel #3252
            Video Games & Consoles #1249
        """

        dict_ebay_location = {
            "england"	    : "EBAY-GB",
            "austria" 	    : "EBAY-AT",
            "france" 	    : "EBAY-FR",
            "germany"	    : "EBAY-DE",
            "italy" 	    : "EBAY-IT",
            "netherlands" 	: "EBAY-NL",
            "spain"	        : "EBAY-ES",
            "ireland" 	    : "EBAY-IE",
            "poland" 	    : "EBAY-PL"
        }

        dict_loc_bay = {
            "EBAY-GB": "England",
            "EBAY-AT": "Austria",
            "EBAY-FR": "France",
            "EBAY-DE": "Germany",
            "EBAY-IT": "Italy",
            "EBAY-NL": "Netherlands",
            "EBAY-ES": "Spain",  
            "EBAY-IE": "Ireland",  
            "EBAY-PL": "Poland"
        }

        tuple_list = []
        not_found_list = []
        for ebay_country in dict_ebay_location.values():
            json_ebay = json.loads(Ebay.country_request(ebay_country,Ebay.KARL_ID, search_word))  
            try:
                for item in range(5):
                    try:
                        currency      = json_ebay["searchResult"]["item"][item]["sellingStatus"]["currentPrice"]["_currencyId"]
                        item_price    = json_ebay["searchResult"]["item"][item]["sellingStatus"]["currentPrice"]["value"]
                        item_name     = json_ebay["searchResult"]["item"][item]["title"]
                        picture_url   = json_ebay["searchResult"]["item"][item]["galleryURL"]

                        if currency != "EUR":
                            in_euro = ForexAndFee.exchange_rate(currency,item_price)
                            price_tuple = (ebay_country, "EUR", float(in_euro), item_name,picture_url)
                            tuple_list.append(price_tuple)
                        else:
                            price_tuple = (ebay_country, "EUR", float(item_price), item_name,picture_url)
                            tuple_list.append(price_tuple)

                    except KeyError as e:
                        print(ebay_country)
                        not_found_list.append(dict_loc_bay[ebay_country])
            except IndexError as e:
                print("- Apparently it didnt find 5 items")
        


        # --> Most expensive item 
        most_expensive = ("","",0,"","")
        for largest in tuple_list:
            if largest[2] > most_expensive[2]:
                most_expensive = largest

        # --> cheapest item 
        cheapest = ("","",999999999999999999,"","")
        for small in tuple_list:
            if small[2] < cheapest[2]:
                cheapest = small


        raw_profit = most_expensive[2] - cheapest[2]
        paypal_fee = ForexAndFee.paypal_fee(most_expensive[2],currency="EUR",selling=True)["EUR"]
        #paypal_fee = ForexAndFee.paypal_fee(most_expensive[2])["EUR"]
        ebay_fee = ForexAndFee.ebay_fee(most_expensive[2])["EUR"]
        real_profit = raw_profit - (paypal_fee + ebay_fee)
        

        # --> possible Profit 
        print("==============================================")
        print(most_expensive[3])
        print("Most Expensive on   : {}".format(most_expensive[0]))
        print("Most expensive Price: {}".format(most_expensive[2]))
        print("---------------------------------")
        print(cheapest[3])
        print("Cheapest on   : {}".format(cheapest[0]))
        print("Cheapest price: {}".format(cheapest[2]))
        print("---------------------------------")
        print("Possible Profit(no fee): {}".format(raw_profit))
        print("Possible Profit (real) : {}".format(real_profit))
        print("")
        #print("Also interesting, a list of Trending items on ebay: {}".format(Ebay.get_trends()))
        #----------------------

        cheap = Cheapest(cheapest[3],cheapest[0],cheapest[2],cheapest[4])
        expen = Expensive(most_expensive[3],most_expensive[0],most_expensive[2],most_expensive[4])
        profit = Profit(raw_profit,paypal_fee,ebay_fee,real_profit)

                
        
        return cheap, expen, profit, not_found_list





#Ebay.get_all_countries_for_item("iphone xr 64")
# Ebay.get_trends()


#-----------------------------------------------------------------
#{
#   'itemId': '163696373484', 
#   'title': 'iPhone XR 64 GB gelb Neugerät von Apple Care', 
#   'globalId': 'EBAY-DE', 

#   'primaryCategory': 
#         {'categoryId': '9355', 
#          'categoryName': 'Handys & Smartphones'},

#    'galleryURL': 'http://thumbs1.ebaystatic.com/m/mRLNfOo41KT8Iq9PFzI24FQ/140.jpg', 
#    'viewItemURL': 'http://www.ebay.de/itm/iPhone-XR-64-GB-gelb-Neugerat-Apple-Care-/163696373484', 
#    'paymentMethod': 'PayPal', 
#    'autoPay': 'true', 
#    'postalCode': '97422', 
#    'location': 'Schweinfurt,Deutschland', 
#    'country': 'DE', 

#    'shippingInfo': 
#         {'shippingServiceCost': 
#                 {'_currencyId': 'EUR', 
#                  'value': '4.99'}, 
#         'shippingType': 'Flat', 
#         'shipToLocations': 'Worldwide'}, 

#   'sellingStatus': 
#         {'currentPrice': 
#                 {'_currencyId': 'EUR',
#                  'value': '600.0'}, 
#         'convertedCurrentPrice': 
#                 {'_currencyId': 'EUR',
#                  'value': '600.0'}, 
#         'sellingState': 'Active', 
#         'timeLeft': 'P21DT20H18M35S'},
#  
#   'listingInfo': 
#         {'bestOfferEnabled': 'false', 
#          'buyItNowAvailable': 'false',
#          'startTime': '2019-05-19T05:01:41.000Z', 
#          'endTime': '2019-06-18T05:01:41.000Z',
#          'listingType': 'FixedPrice', 
#          'gift': 'false', 
#          'watchCount': '6'}, 

#   'condition': 
#         {'conditionId': '1500',
#          'conditionDisplayName': 'Neu: Sonstige (siehe Artikelbeschreibung)'}, 

#   'isMultiVariationListing': 'false', 
#   'topRatedListing': 'false', 
#   'eBayPlusEnabled': 'false'
# }
#-----------------------------------------------------------------

