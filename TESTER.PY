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

try:
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    print("Database Successfully Connected to SQLite")
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
cursor.execute("""SELECT * From Notifications""")
records = cursor.fetchall()

for reader in records:
    print(reader[1])
    print(reader[2])
    url = reader[1]
    name = reader[2]
    #opening the page
    connecting = browser.get(url)
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
    print(price1)
    price2 = re.findall("\d*\.\d*\d", str(price1))
    #<title>DAI $1.00907830 - Pair Explorer - DEXTools.io - BETA</title>
    price = float(listcleaner(price2))
    print(price)
    browser.quit()

    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    acccount_sid = 'ACcb2e453e9bd412cafdd544f39da1d20a'
    auth_token = 'd3ce983e57884c658aa0f122a2cf1493' 

    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body=f'Notyfikacja odnosnie {name}',
            from_='+15017122661',
            to='+48725583900'
        )

    print(message.sid)

#print("something went wrong!")
"""
f=open("logtest.txt", "w+")
now = datetime.now()
f.write("scripped started runnings" + str(now) + str(soup)  + '\n')
print("now =" + str(now) + "log printed")
"""
