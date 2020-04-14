import tweepy
import pickle 
from fake_useragent import UserAgent
import SQLite_util as sqlutil
import re


def random_header():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    return(headers)


def get_dbconn():
    database = "C:\\Users\\karlm\\Google Drive\\Coding\\easyBay-Arbitrage\\twitterdeals.db"
    sqlutil.make_db(database)
    conn = sqlutil.create_connection(database)


    sql_create_tweets_table = """ CREATE TABLE IF NOT EXISTS tweets (
                                        id integer PRIMARY KEY,
                                        id_str text NOT NULL, 
                                        created_at text NOT NULL, 
                                        full_text text NOT NULL, 
                                        username text NOT NULL, 
                                        lang text NOT NULL
                                    ); """
    
    sqlutil.create_table(conn, sql_create_tweets_table)

    return conn 


def insert_tweet(conn, tweet_tuple):
    cur = conn.cursor()
    sql = 'INSERT INTO tweets VALUES (id_str, created_at, full_text, username, lang) VALUES(?,?,?,?,?)'
    cur.execute(sql, tweet_tuple)

    conn.commit()
    return cur.lastrowid


def tweet_in_db(conn, tweet_tuple):
    tweet_id = tweet_tuple[0]
    sql = "SELECT count(*) as count FROM tweets WHERE id_str = '{0}'".format(tweet_id)

    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    
    in_db = rows[0][0]

    if in_db > 0:
        return True
    else:
        return False




def get_tweets(num_tweets, twitter_users):

    list_of_tweets = []

    with open('tokens_twitter.pickle', 'rb') as handle:
        tokens = pickle.load(handle)

    cons_key = tokens["cons_key"] 
    cons_sec = tokens["cons_sec"] 
    accs_tok = tokens["accs_tok"] 
    accs_sec = tokens["accs_sec"] 

    auth = tweepy.OAuthHandler(cons_key, cons_sec)
    auth.set_access_token(accs_tok, accs_sec)
    api = tweepy.API(auth)


    for twitter_user in twitter_users:
        tweets = api.user_timeline(screen_name = twitter_user, count = num_tweets, tweet_mode = 'extended',exclude_replies = True)



        for tweet in tweets:
            try:
                tweet_tuple = (tweet._json["id_str"],tweet._json["created_at"],tweet._json["full_text"],tweet._json["user"]["screen_name"],tweet._json["lang"])
                list_of_tweets.append(tweet_tuple)

            except AttributeError:
                tweet_tuple = (tweet._json["id_str"],tweet._json["created_at"],tweet._json["full_text"],tweet._json["user"]["screen_name"],tweet._json["lang"])
                list_of_tweets.append(tweet_tuple)
    
    return list_of_tweets



def get_rabatt(tweet_tuple):
    tweet_text = tweet_tuple[2]
    tweet_lang = tweet_tuple[4]

    if tweet_lang == "de":
            
        save_ger_regex = r" (\d+)% Rabatt"
        matches_ger = re.findall(save_ger_regex, tweet_text)

        ger_rabatt = (matches_ger[0][0],matches_ger[0][1])
        return ger_rabatt

    if tweet_lang == "en":
        save_uk_regex = r"(\d+%)|(Save)"
        matches_uk = re.findall(save_uk_regex, tweet_text)

        uk_save = (matches_uk[0][0],matches_uk[0][1])
        return uk_save


def get_superpunkte(tweet_tuple):
    tweet_text = tweet_tuple[2]
    tweet_lang = tweet_tuple[4]

    if tweet_lang == "de":
        regex_ger = r" (\d+)-fache Superpunkte"
        match_ger = re.findall(regex_ger, tweet_text)

        ger_super = (match_ger[0][0],match_ger[0][1])
        return ger_super

    
    if tweet_lang == "en":
        regex_eng = r"(\d+%)|(Super Points)"
        match_eng = re.findall(regex_eng, tweet_text)

        eng_super = (match_eng[0][0],match_eng[1][1])
        return eng_super
        





def get_deal_url(tweet_tuple):
    tweet_text = tweet_tuple[2]
    print(tweet_text)
    pass

def main():

    choice = {"rakuten":["RakutenUK","Rakuten_GER"],
              "monsterdealz": ["MonsterDealz"],
              "dealsniper":["snipz"],
              "sparfuchs":["fuchsfeed"],
              "dealdoktor":["dealdoktor"]
              }

    rakuten_tweets = get_tweets(10, choice["rakuten"])
    
    for rakuten_tweet in rakuten_tweets:
        get_deal_url(rakuten_tweet)
        print(get_rabatt(rakuten_tweet))
        print(get_superpunkte(rakuten_tweet))

        # Current output:
        """
        Save 20% on a huge range of #LEGO sets + get 3% of your spend back in Super Points!
        Only at https://t.co/pgi9nd88cb https://t.co/wWJOsfrosm
        ('', 'Save')
        ('20%', '')
        Spring into the outdoors with this week's DECATHLON Special! Save BIG on sports #shoes, sports #gear, sports #equipment and much more!
        Plus, when you shop at DECATHLON today, we'll give you 10% of your purchase price back in Super Points!
        https://t.co/gEwtHfPmJ8
        #easterspecial https://t.co/skIwvjImk0
        ('', 'Save')
        ('10%', 'Super Points')
        From unbelievable bundle deals on #consoles to the hottest new releases, check out the amazing #offers at GAME this week!
        On top of great #discounts, you'll get 6% of your purchase back in Super Points, when you #shop at GAME today!
        https://t.co/A95VDtF6UR
        #uk #gaming #ps4 https://t.co/fwsZwrCK25
        ('6%', '')
        ('6%', 'Super Points')


        """


main()
