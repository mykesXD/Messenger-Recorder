# -*- coding: utf-8 -*-
from os import system
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import io
from getpass import getpass
import stdiomask

user_email = input("Email: ")
user_password = stdiomask.getpass()
print("1. Go to 'facebook.com' or 'messenger.com'")
print("2. Open the chat you want to record on a new tab")
print("3. Copy the link (should be a URL ending with '/t/xxxxxxxxx')")
user_messenger = input("4. Paste it Here->: ")
chatType = user_messenger.split('/')

system("cls")

print("\nMessages will be stored inside messages.txt")
print("\n KEEP THIS CONSOLE AND CHROME WINDOW OPEN, MINIMIZED")
print("\n CLOSING WILL EXIT THE APPLICATION")

PATH = "driver/chromedriver"
driver = webdriver.Chrome(PATH)
driver.minimize_window()

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

def saveMessage():
    waitTime = 6
    while True:
        lastMessage = "i wanna die"
        today = datetime.now()
        date = today.strftime("%m/%d,%H:%M")
        time.sleep(waitTime)
        try:
            name = driver.find_element_by_css_selector("div[role=row]:last-child>div>div[role=gridcell]>h4>span")
        except:
            try:
                name = driver.find_element_by_css_selector("div[role=row]:last-child>div>div[role=gridcell]>h4>div>div")
            except:
                saveMessage()
        name = name.text
        try:
            with io.open('messages.txt', 'r', encoding='utf8') as f:
                reader = f.read()
                reader = list(reader.split('\n'))
                reader = reader[-2].split(' - ')
                lastMessage = reader[1].strip('"')
        except:
            pass
        try: #This code is just pathetic someone pls kill me
            try:
                messages = driver.find_elements_by_css_selector("div[dir=auto]:last-of-type")[-1]
            except:
                try:
                    messages = driver.find_elements_by_css_selector("div[dir=auto]")[-1]
                except:
                    saveMessage()
            messages = messages.text
            if messages != lastMessage:
                with io.open('messages.txt', 'a', encoding='utf8') as f:
                    text = name + ' - "' + messages + '" - ' + date + "\n"
                    f.write(text)
                    print(text)
                    waitTime = 2
        except:
            pass

saveMessage()
driver.quit()