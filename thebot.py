import requests
from bs4 import BeautifulSoup
from lxml import html
import math
import re
import pymysql
import fileinput
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from datetime import date
from datetime import datetime
import sqlite3
from twilio.rest import Client
from time import sleep


# Date/ time info
today1 = date.today()
today = str(today1)
currentMonth = datetime.now().month
currentYear = datetime.now().year

def listcleaner(texttoclean):
    cleaning1 = str(texttoclean)
    cleaning2 = cleaning1.lstrip('[\' ')
    cleaning = cleaning2.rstrip('\']')
    return cleaning

print("starting ")
chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome('chromedriver', options=chrome_options)
global url
global name
browser.close
browser.quit
try:
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        print("Database Successfully Connected to SQLite")
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    cursor.execute("""SELECT * From Notifications""")
    records = cursor.fetchall()
    for reader in records:
        print(reader[0])
        print(reader[1])
        print(reader[2])
        print(reader[3])
        name = reader[1]
        url = str(reader[2])
        biggerthan = reader[3]
        smallerthan = reader[4]
        PhoneNumber = str(reader[5])
        #opening the page
        #url = "https://www.dextools.io/app/uniswap/pair-explorer/0xa478c2975ab1ea89e8196811f51a7b7ade33eb11?fbclid=IwAR1flnUZAM_WD94UIY2wOJW7yaN5jiaBNqmdhNVV6cTeHVjLhxk-QWUJV7E"
        connecting = browser.get(url)
        sleep(300)
        results = browser.page_source
        soup = BeautifulSoup(results, "lxml")
        try:
            myElem = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, r'/html/body/app-root/div[2]/div/main/app-uniswap/div/app-pairexplorer/app-layout/div/div/div[2]/div[1]/div/div[2]/ul/li[2]')))
            print("the website is ready")
        except TimeoutException:
            print("website took too much time!")
        results = browser.page_source
        soup = BeautifulSoup(results, "lxml")

        price1 = soup.find("title")
        price2 = re.findall("\d*\.\d*\d", str(price1))
        #<title>DAI $1.00907830 - Pair Explorer - DEXTools.io - BETA</title>
        price = float(listcleaner(price2))
        browser.close()
        browser.quit()
        print("price")
        print(price)
        print("smallerthan")
        print(smallerthan)
        print("biggerthan")
        print(biggerthan)
        print("phone number")
        print(PhoneNumber)
        if price < smallerthan or  price > biggerthan: 
        # Your Account Sid and Auth Token from twilio.com/console
        # DANGER! This is insecure. See http://twil.io/secure
            account_sid = 'ACcb2e453e9bd412cafdd544f39da1d20a'
            auth_token = 'd3ce983e57884c658aa0f122a2cf1493' 
            client = Client(account_sid, auth_token)
            message = client.messages \
                .create(
                    body=f'Notyfikacja odnosnie {name} obecna cena to {price}. Parametry: Cena powinna byc mniejsza od{smallerthan} i wieksza od {biggerthan}',
                    from_='+14254092949',
                    to='+48' + str(PhoneNumber)
                )
            print(message.sid)
            print("message sent")
except Exception as ex:
    browser.close()
    browser.quit()
    print(ex) 
    try:
        f=open("logerrors.txt", "w+")
        now = datetime.now()
        f.write("scripped started running" + str(now) + str(ex) + '\n')
    except:
        browser.close()
        browser.quit()
        pass
