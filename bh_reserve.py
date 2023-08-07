from bs4 import BeautifulSoup
import requests
import sys
from datetime import datetime, timedelta

import json
import os.path
from os import path
import glob
import time
import smtplib
import platform
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import re
import traceback


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


from pyvirtualdisplay import Display

#load .env file with dotenv
from dotenv import load_dotenv
load_dotenv()

display= None
driver = None
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

ENABLE_EMAIL = True

BH_USER = os.getenv('BH_USER')
BH_PASSWORD = os.getenv('BH_PASSWORD')
SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_TO = os.getenv('SMTP_TO')
SMTP_FROM = os.getenv('SMTP_FROM')
SEARCHTERMS = json.loads(os.environ['SEARCHTERMS'])



print(SEARCHTERMS)
from pathlib import Path

lastimage=None

# this function takes a screenshot of the current web page and saves it to the current directory
def screenshot(title):
    if driver!=None:
        global lastimage 
        lastimage=f"{current_time}_{title}.png"
        driver.get_screenshot_as_file(lastimage)
        
i=0

try:

    def send_mail(
        to_email,
        subject,
        message,
        message_html=None,
        server=SMTP_HOST,
        from_email=SMTP_FROM,        
        imageFN=None
    ):
        if ENABLE_EMAIL:
            # Create message container - the correct MIME type is multipart/alternative.
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = from_email
            msg["To"] = to_email
            msg["CC"] = to_email

            part1 = MIMEText(message, "plain")
            msg.attach(part1)
            if message_html != None:
                part2 = MIMEText(message_html, "html")
                msg.attach(part2)

            if imageFN!=None:
                with open(imageFN, 'rb') as f:
                    img_data = f.read()                
                    image = MIMEImage(img_data, name=os.path.basename(imageFN))
                    msg.attach(image)                
            server = smtplib.SMTP(server)
            # server.set_debuglevel(1)
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()

    import pickle

    

    entries = {}

    
    if path.exists("/data/buecherhalle.pkl"):
        with open("/data/buecherhalle.pkl", "rb") as f:
            entries = pickle.load(f)
            print("/data/buecherhalle.pkl loaded. Entries: "+str(len(entries)))
    tod = datetime.now()
    d = timedelta(days=-7)
    a = tod - d
    datestring = a.strftime("%Y-%m-%d")

    main_url = "https://www.onleihe.de/hamburg/frontend/mediaList,0-0-0-101-0-0-0-2008-400005-0-0.html"
    
    req = requests.post(
        main_url,
        json=None,
        proxies=None,
        timeout=30,
    )

    bs = BeautifulSoup(req.text, "html.parser")



    sr = bs.find("h3", class_="card-title")

    
    while sr:
        link = sr.findNext("a", class_="link")
        for searchterm in SEARCHTERMS:
            if sr.text.find(searchterm) > -1 and sr.text not in entries:
                i=i+1
                i_s=str(i)
                print('Searchterm '+searchterm+' hits '+ sr.text)
                entries[sr.text] = 1
                
                if display==None:
                    print('Starting display')
                    display = Display(visible=0, size=(800, 800))  
                    display.start()



                    chromeOptions = webdriver.ChromeOptions() 
                    # chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) 
                    chromeOptions.add_argument("--no-sandbox") 
                    chromeOptions.add_argument("--disable-setuid-sandbox") 

                    chromeOptions.add_argument("--remote-debugging-port=9222")  # this

                    chromeOptions.add_argument("--disable-dev-shm-using") 
                    chromeOptions.add_argument("--disable-extensions") 
                    # chromeOptions.add_argument("--disable-gpu") 
                    chromeOptions.add_argument("start-maximized") 
                    # chromeOptions.add_argument("disable-infobars")
                    chromeOptions.add_argument(r"user-data-dir=.\cookies\\test") 

                    driver = webdriver.Chrome(options=chromeOptions)
                    #Login
                    driver.get("https://www.onleihe.de/hamburg/frontend/myBib,0-0-0-100-0-0-0-0-0-0-0.html")
                    screenshot(i_s+"1_pre_login")
                    cookie_accept=driver.find_element(By.CLASS_NAME, "privacyAcceptAll")
                    
                    if cookie_accept!=None:
                        print('Cookie accept')
                        try:
                            cookie_accept.click()
                            driver.execute_script("arguments[0].click();", cookie_accept)
                            driver.implicitly_wait(4)
                            print('Cookie accept ok')
                        except:
                            print('Cookie accept failed')
                            exit()
                    screenshot(i_s+"2_after_cookie")
                    userName=driver.find_element(By.ID, "userName")
                    password=driver.find_element(By.ID, "password")
                    if userName== None:
                        print('username field not found')    
                        exit()
                    if password== None:
                        print('password field not found')    
                        exit()
                    print('username and password field found')
                    driver.execute_script("arguments[0].scrollIntoView();", password)
                    #screenshot(i_s+"2a_after_cookie_scrollinview")
                    password.clear()
                    password.send_keys(BH_PASSWORD)

                    userName.clear()
                    userName.send_keys(BH_USER)

                    print('Login in')
                    password.send_keys(Keys.RETURN)
                    driver.implicitly_wait(4)
                    screenshot(i_s+"3_after_login")
                    logout= driver.find_element(By.PARTIAL_LINK_TEXT, "Logout")
                    assert logout!=None
                    print('Logged in')

                driver.get('https://www.onleihe.de/hamburg/frontend/'+link.attrs['href'])
                screenshot(i_s+"4_after_media_browse")
                vormerken=None
                try:
                    vormerken = driver.find_element(By.PARTIAL_LINK_TEXT, "Vormerken")
                except:
                    None
                ausleihen=None
                try:
                    ausleihen = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div/div[1]/div[2]/div/div[4]/div[2]/form/div/button')
                except:
                    None
                if ausleihen!=None:
                    print("Ausleihen found")
                    driver.execute_script("arguments[0].scrollIntoView();", ausleihen)
                    driver.execute_script("arguments[0].click();", ausleihen)
                    print("Ausleihen clicked")
                    screenshot(i_s+"5_after_ausleihen")
                    send_mail(
                    "mm@marcusmoennig.de",
                    "Buecherhalle Update - Ausgeliehen: " + sr.text,
                    "Buecherhalle Update - Ausgeliehen: " + sr.text,
                    "Buecherhalle Update - Ausgeliehen: " + sr.text,
                    )
                else:
                    if vormerken!=None:                        
                        print("Vormerken found")
                        l=vormerken.get_attribute("href")
                        driver.get(l)
                        print("Vormerken page got")
                        pRecipient=driver.find_element(By.ID, "pRecipient")
                        pConfirmedRecipient=driver.find_element(By.ID, "pConfirmedRecipient")
                        driver.execute_script("arguments[0].scrollIntoView();", pConfirmedRecipient)

                        pRecipient.send_keys(SMTP_TO)
                        pConfirmedRecipient.send_keys(SMTP_TO)
                        print("Email filled")
                        driver.implicitly_wait(2)
                        screenshot(i_s+"5_after_email_filled")
                        vormerken2 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div/div/div[4]/button')
                        driver.execute_script("arguments[0].scrollIntoView();", vormerken2)
                        driver.execute_script("arguments[0].click();", vormerken2)
                        screenshot(i_s+"6_after_vormerken_clicked")
                        print("Vormerken clicked")

                        send_mail(
                        SMTP_TO,
                        "Buecherhalle Update - Vorgemerkt: " + sr.text,
                        "Buecherhalle Update - Vorgemerkt: " + sr.text,
                        "Buecherhalle Update - Vorgemerkt: " + sr.text,
                        )
                if ausleihen==None and vormerken==None:
                    print('Vormerklimit erreicht')
                print('***************************************')
        entries[sr.text] = 1

             
        sr = sr.find_next("h3", class_="card-title")

    with open("/data/buecherhalle.pkl", "wb") as f:
        pickle.dump(entries, f)
        print("/data/buecherhalle.pkl saved. Entries: "+str(len(entries)))

    files_to_delete = glob.glob(current_time+"*")
    for file_path in files_to_delete:
        os.remove(file_path)

except Exception as E:
    text = str(E) + "\n\n" + traceback.format_exc()
    send_mail(SMTP_TO, "Exception searching for buecherhallen update ", text, imageFN=lastimage)
    print(str(E) + "\n\n" + traceback.format_exc())
    screenshot(str(i)+"9_exception")