# -*- coding: utf-8 -*-
from os import system
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import io
from getpass import getpass
import stdiomask
from win10toast import ToastNotifier
from rich.console import Console, OverflowMethod
from rich.table import Table

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

options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome('driver/chromedriver', options=options)
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
toast = ToastNotifier()
deletedMessages = []
lastMessage = "i wanna die"
table = Table(title="Chat")
table.add_column("Names", justify="right", style="bold cyan", no_wrap=True)
table.add_column("Messages", style="white", overflow="fold")
table.add_column("Time", justify="left", style="green")
console = Console()
messageType = "text"
messageWasDeleted = False
time.sleep(5)
def unsentCheck(date):
    global messageWasDeleted
    with io.open('messages.txt', 'r', encoding='utf8') as f:
        reader = f.read()
        reader = list(reader.split('\n'))
        readerList = reader
    for i in range(1,5):
        deleteCheck = driver.find_element_by_css_selector(f"div[data-testid='mw_message_list']>:nth-last-child({i}) div[data-testid='message-container']>div>div>span>div").text
        deletedMessage = readerList[-(i+1)].split(' | ')[1].strip('"')
        msgType = readerList[-(i+1)].split(' | ')[3].strip('"')
        if 'unsent a message' in deleteCheck and deletedMessage not in deletedMessages:
            msg = readerList[-(i+1)].split(' | ')[1].strip('"')
            if msgType == "text":
                table.add_row(f"[bold red]{deleteCheck}",msg, date)
            elif msgType == "image":
                table.add_row(f"[bold red]{deleteCheck}",f"[link={msg}]Image File[/link]", date)
            elif msgType == "video":
                table.add_row(f"[bold red]{deleteCheck}",f"[link={msg}]Video File[/link]", date)
            elif msgType == "link":
                table.add_row(f"[bold red]{deleteCheck}",f"[link={msg}]Link URL[/link]", date)
            elif msgType == "audio":
                table.add_row(f"[bold red]{deleteCheck}",f"[link={msg}]Audio File[/link]", date)
            toast.show_toast("MESSAGE DELETED",readerList[-(i+1)].split(' | ')[0] + ":" + readerList[-(i+1)].split(' | ')[1],duration=5,icon_path="messenger-logo.ico")
            deletedMessages.append(deletedMessage)
            with io.open('messages.txt', 'r', encoding='utf8') as f:
                reader = f.readlines()
                reader[-i] = reader[-i].split("\n")[0] + " - DELETED\n"
            with io.open('messages.txt', 'w', encoding='utf8') as f:
                f.writelines(reader)
            messageWasDeleted = True
    if(messageWasDeleted == True):
        system("cls")
        console.print(table)
        messageWasDeleted = False
def saveMessage():
    while True:
        today = datetime.now()
        date = today.strftime("%I:%M%p,%b %d")
        time.sleep(0.1)
        try:
            with io.open('messages.txt', 'r', encoding='utf8') as f:
                reader = f.read() #when can i die from being so dumb
                reader = list(reader.split('\n'))
                reader = reader[-2].split(' | ')
                lastMessage = reader[1].strip('"')
        except:
            pass
        try: #This code is just pathetic someone pls kill me
            try:
                messages = driver.find_element_by_css_selector("div[data-testid='mw_message_list']>:last-child div[dir=auto] span a").text.replace("\n"," ")
                messageType = "link"
            except:
                try:
                    messages = driver.find_element_by_css_selector("div[data-testid='mw_message_list']>:last-child div[dir=auto]").text.replace("\n"," ")
                    messageType = "text"
                except:
                    try:
                        messages = driver.find_element_by_css_selector("div[data-testid='mw_message_list']>:last-child img[alt='Open Photo']").get_attribute("src")
                        messageType = "image"
                    except:
                        try:
                            messages = driver.find_element_by_css_selector("div[data-testid='mw_message_list']>:last-child video[playsinline]").get_attribute("src")
                            messageType = "video"
                        except:
                            try:
                                messages = driver.find_element_by_css_selector("div[data-testid='mw_message_list']>:last-child audio").get_attribute("src")
                                messageType = "audio"
                            except:
                                try:
                                    unsentCheck(date)
                                except:
                                    pass
            try:
                name = driver.find_element_by_css_selector("div[data-testid='mw_message_list']>:last-child div div h4 span")
            except:
                try:
                    name = driver.find_element_by_css_selector("div[data-testid='mw_message_list']>:last-child div div h4 div div")
                except:
                    pass
            name = name.text
            if messages != lastMessage:
                with io.open('messages.txt', 'a', encoding='utf8') as f:
                    text = name + ' | "' + messages + '" | ' + date + ' | ' + messageType + "\n"
                    f.write(text)
                    if messageType == "text":
                        table.add_row(name,messages, date)
                    elif messageType == "image":
                        table.add_row(name,f"[link={messages}]Image File[/link]", date)
                    elif messageType == "video":
                        table.add_row(name,f"[link={messages}]Video File[/link]", date)
                    elif messageType == "link":
                        table.add_row(name,f"[link={messages}]Link URL[/link]", date)
                    elif messageType == "audio":
                        table.add_row(name,f"[link={messages}]Audio File[/link]", date)
                    system("cls")
                    console.print(table)
        except:
            pass
        try:
            unsentCheck(date)
        except:
            pass

saveMessage()
driver.quit()
