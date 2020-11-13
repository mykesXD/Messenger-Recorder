# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date
import time
import csv
import io
user_email = input("Email: ")
user_password = input("Password: ")
print("1. Go to www.messenger.com")
print("2. Login")
print("3. Go to the chat you want to record")
print("4. Copy the link (Ex. https://www.messenger.com/t/xxxxxxxx)")
user_messenger = input("5. Paste it Here->: ")
print("\nMessages will be stored inside (messages.txt) file")
print("\n DO NOT CLOSE THIS CONSOLE AND CHROME WINDOW!")
today = date.today()
date = today.strftime("%Y/%m/%d")
PATH = "C:/Program Files (x86)/chromedriver.exe" #Download ChromeDriver version same as your Chrome Browser version and put the path here
driver = webdriver.Chrome(PATH)
driver.get(user_messenger)
time.sleep(2)
email = driver.find_element_by_id("email")
email.send_keys(user_email)
time.sleep(2)
password = driver.find_element_by_id("pass")
password.send_keys(user_password)
time.sleep(2)
loginButton = driver.find_element_by_id("loginbutton")
loginButton.send_keys(Keys.RETURN)
lastMessage = 'i wanna die this is not a joke this is a cry for help'
while True:
    time.sleep(2)
    name = driver.find_element_by_css_selector("div#js_1>:last-child>div>:last-child>:first-child")
    name = name.text
    try:
        with io.open('messages.txt', 'r', encoding='utf8') as f:
            reader = f.read()
            reader = list(reader.split('\n'))
            reader = reader[-2].split(';')
            lastMessage = reader[1]
    except:
        pass
    try: #This code is just pathetic someone pls kill me
        messages = driver.find_element_by_css_selector("div#js_1>:last-child>div>:last-child>:last-child>div>:last-child>span")
        messages = messages.text
        if messages != lastMessage:
            with io.open('messages.txt', 'a', encoding='utf8') as f:
                text = name + ';' + messages + ';' + date + "\n"
                writer = f.write(text)
                print(text)

    except:
        pass
driver.quit()
