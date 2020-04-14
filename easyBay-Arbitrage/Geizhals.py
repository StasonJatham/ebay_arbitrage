"""
import requests
from fake_useragent import UserAgent
def random_header():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    return(headers)

test = requests.get("https://geizhals.eu/apple-iphone-8-plus-64gb-grau-a1688630.html#offerlist", headers=random_header())

print(test.text)
#funktioniert nicht
"""

from selenium import webdriver
import time  
from selenium.webdriver import ActionChains  
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# IF LAZY LOAD ----> driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def get_top_ten():
    # Current Output
    """
    --------------------------------
    ab € 275,37
    Samsung Galaxy S8 G950F schwarz
    in Handys ohne Vertrag
    https://geizhals.eu/samsung-galaxy-s8-g950f-schwarz-sm-g950fzka-a1601178.html#ang
    https://geizhals.eu/samsung-galaxy-s8-g950f-schwarz-sm-g950fzka-a1601178.html
    https://geizhals.eu/?cat=umtsover
    --------------------------------
    ab € 18,85
    Crucial BX500 120GB, SATA
    in Solid State Drives (SSD)
    https://geizhals.eu/crucial-bx500-120gb-ct120bx500ssd1-a1875722.html#ang
    https://geizhals.eu/crucial-bx500-120gb-ct120bx500ssd1-a1875722.html
    https://geizhals.eu/?cat=hdssd
    --------------------------------
    """

    driver=webdriver.Firefox()
    driver.get("https://geizhals.eu")

    wait = WebDriverWait(driver, 12)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.productOffers-list.productOffers-list--dActive")))
    #wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.teaserbox")))
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.teaserbox")))
    


    element = driver.find_element_by_id("gh_m_top")
    products = element.find_elements_by_tag_name("li")

    for item in products:
        item_links = item.find_elements_by_tag_name('a')
        text = item.text
        print("--------------------------------")
        print(text)
        for link in item_links:
            print(link.get_attribute("href"))

    driver.close()
    driver.quit()


def get_cheap_phones(phone_link="https://geizhals.eu?cat=umtsover"):
        # Current Output
    """
    --------------------------------
    Apple iPhone 6s 32GB grau
    Betriebssystem: iOS 12.1 (via Update) • Display: 4.7", 1334x750 Pixel, 16 Mio. Farben, IPS, kapazitiver Touchscreen, druckempfindlich • Kamera hinten: 12.0MP, f/2.2, Phasenvergleich-AF, Dual-LED-Blitz, Videos @2160p/30fps • Kamera vorne: 5.0MP, ...
    https://geizhals.eu/apple-iphone-6s-32gb-grau-a1505269.html?hloc=at&hloc=de&hloc=eu&hloc=pl&hloc=uk
    --------------------------------
    Betriebssystem: iOS 12.1 (via Update) • Display: 4.7", 1334x750 Pixel, 16 Mio. Farben, IPS, kapazitiver Touchscreen, druckempfindlich • Kamera hinten: 12.0MP, f/2.2, Phasenvergleich-AF, Dual-LED-Blitz, Videos @2160p/30fps • Kamera vorne: 5.0MP, ...
    --------------------------------
    4.8
    137 Bewertungen
    https://geizhals.eu/?sr=1505269,-1
    --------------------------------
    4.8
    137 Bewertungen
    --------------------------------
    4.8
    --------------------------------
    181
    --------------------------------

    --------------------------------

    --------------------------------
    ab € 292,95
    --------------------------------
    Mindfactory
    https://geizhals.eu/apple-iphone-6s-32gb-grau-a1505269.html?hloc=at&hloc=de&hloc=eu&hloc=pl&hloc=uk#ang
    --------------------------------

    #====== this comment is not part of the output =======================================================================

    Samsung Galaxy S8+ G955F schwarz (SM-G955FZKA)
    Betriebssystem: Android 9.0 (via Update) • Display: 6.2", 2960x1440 Pixel, 16 Mio. Farben, AMOLED, kapazitiver Touchscreen, druckempfindlich (partiell), Gorilla-Glas 5, HDR (HDR10) • Kamera hinten: 12.0MP, f/1.7, Phasenvergleich-AF (Dual-Pixel), ...
    4.8
    603 Bewertungen
    71 ab € 303,58 gadget-outlet
    https://geizhals.eu/samsung-galaxy-s8-g955f-schwarz-sm-g955fzka-a1601215.html?hloc=at&hloc=de&hloc=eu&hloc=pl&hloc=uk
    https://geizhals.eu/samsung-galaxy-s8-g955f-schwarz-sm-g955fzka-a1601215.html?hloc=at&hloc=de&hloc=eu&hloc=pl&hloc=uk
    https://geizhals.eu/?sr=1601215,-1
    https://geizhals.eu/samsung-galaxy-s8-g955f-schwarz-sm-g955fzka-a1601215.html?hloc=at&hloc=de&hloc=eu&hloc=pl&hloc=uk#ang
    --------------------------------

    --------------------------------

    --------------------------------

    --------------------------------

    https://geizhals.eu/samsung-galaxy-s8-g955f-schwarz-sm-g955fzka-a1601215.html?hloc=at&hloc=de&hloc=eu&hloc=pl&hloc=uk
    --------------------------------

    --------------------------------
    Samsung Galaxy S8+ G955F schwarz (SM-G955FZKA)
    Betriebssystem: Android 9.0 (via Update) • Display: 6.2", 2960x1440 Pixel, 16 Mio. Farben, AMOLED, kapazitiver Touchscreen, druckempfindlich (partiell), Gorilla-Glas 5, HDR (HDR10) • Kamera hinten: 12.0MP, f/1.7, Phasenvergleich-AF (Dual-Pixel), ...
    https://geizhals.eu/samsung-galaxy-s8-g955f-schwarz-sm-g955fzka-a1601215.html?hloc=at&hloc=de&hloc=eu&hloc=pl&hloc=uk
    --------------------------------
    Betriebssystem: Android 9.0 (via Update) • Display: 6.2", 2960x1440 Pixel, 16 Mio. Farben, AMOLED, kapazitiver Touchscreen, druckempfindlich (partiell), Gorilla-Glas 5, HDR (HDR10) • Kamera hinten: 12.0MP, f/1.7, Phasenvergleich-AF (Dual-Pixel), ...
    --------------------------------
    4.8
    603 Bewertungen
    https://geizhals.eu/?sr=1601215,-1
    --------------------------------
    4.8
    603 Bewertungen
    --------------------------------
    4.8
    --------------------------------
    71
    --------------------------------

    --------------------------------

    --------------------------------
    ab € 303,58
    --------------------------------
    gadget-outlet
    https://geizhals.eu/samsung-galaxy-s8-g955f-schwarz-sm-g955fzka-a1601215.html?hloc=at&hloc=de&hloc=eu&hloc=pl&hloc=uk#ang


    #====== this comment is not part of the output =======================================================================


    --------------------------------
    Xiaomi Mi 9 128GB blau
    Betriebssystem: Android 9.0 • Display: 6.39", 2340x1080 Pixel, 16 Mio. Farben, AMOLED, kapazitiver Touchscreen, Gorilla-Glas 6, Aussparung, HDR (HDR10) • Kamera hinten: 48.0MP, f/1.75, Kontrast-AF, Laser-AF, Phasenvergleich-AF, Dual-LED-Blitz, ...
    (zu wenige) 63 ab € 434,11 Amazon.de
    https://geizhals.eu/xiaomi-mi-9-128gb-blau-a1995036.html?hloc=at&hloc=de&hloc=eu&hloc=pl&hloc=uk
    https://geizhals.eu/xiaomi-mi-9-128gb-blau-a1995036.html?hloc=at&hloc=de&hloc=eu&hloc=pl&hloc=uk
    https://geizhals.eu/?sr=1995036,-1
    https://geizhals.eu/xiaomi-mi-9-128gb-blau-a1995036.html?hloc=at&hloc=de&hloc=eu&hloc=pl&hloc=uk#ang
    --------------------------------

    --------------------------------

    --------------------------------

    --------------------------------

    https://geizhals.eu/xiaomi-mi-9-128gb-blau-a1995036.html?hloc=at&hloc=de&hloc=eu&hloc=pl&hloc=uk
    --------------------------------

    --------------------------------
    Xiaomi Mi 9 128GB blau
    Betriebssystem: Android 9.0 • Display: 6.39", 2340x1080 Pixel, 16 Mio. Farben, AMOLED, kapazitiver Touchscreen, Gorilla-Glas 6, Aussparung, HDR (HDR10) • Kamera hinten: 48.0MP, f/1.75, Kontrast-AF, Laser-AF, Phasenvergleich-AF, Dual-LED-Blitz, ...
    https://geizhals.eu/xiaomi-mi-9-128gb-blau-a1995036.html?hloc=at&hloc=de&hloc=eu&hloc=pl&hloc=uk
    --------------------------------
    Betriebssystem: Android 9.0 • Display: 6.39", 2340x1080 Pixel, 16 Mio. Farben, AMOLED, kapazitiver Touchscreen, Gorilla-Glas 6, Aussparung, HDR (HDR10) • Kamera hinten: 48.0MP, f/1.75, Kontrast-AF, Laser-AF, Phasenvergleich-AF, Dual-LED-Blitz, ...
    --------------------------------
    (zu wenige)
    https://geizhals.eu/?sr=1995036,-1
    --------------------------------
    63
    --------------------------------

    --------------------------------

    --------------------------------
    ab € 434,11
    --------------------------------
    Amazon.de
    https://geizhals.eu/xiaomi-mi-9-128gb-blau-a1995036.html?hloc=at&hloc=de&hloc=eu&hloc=pl&hloc=uk#ang
    --------------------------------
    """

    driver=webdriver.Firefox()
    driver.get(phone_link)

    #wait = WebDriverWait(driver, 12)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.productOffers-list.productOffers-list--dActive")))
    #wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.teaserbox")))
    #wait.until(EC.visibility_of_element_located((By.ID, "lazy-list--categoryList")))

    time.sleep(5) # ---> lazy load is too lazy, needs some time after scrolling
    
    element = driver.find_element_by_id("lazy-list--categorylist")
    products = element.find_elements_by_tag_name("div")

    for item in products:
        item_links = item.find_elements_by_tag_name('a')
        text = item.text
        print("--------------------------------")
        print(text)
        for link in item_links:
            print(link.get_attribute("href"))

    driver.close()
    driver.quit()

get_cheap_phones()