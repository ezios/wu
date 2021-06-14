#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys

PHONE_NUMBER = ""
if not PHONE_NUMBER:
    print("Initialiser la variable PHONE_NUMBER à la ligne 10 du code, merci")
    sys.exit()

def login():
    browser = webdriver.Firefox(executable_path='C:/Temp/geckodriver.exe')
    browser.get("https://web.telegram.org/#/login")
    phone_input_number = browser.find_element_by_name("phone_number")
    phone_number = PHONE_NUMBER
    phone_input_number.clear()
    phone_input_number.send_keys(phone_number + Keys.ENTER)
    ok = browser.find_element_by_css_selector('.btn.btn-md.btn-md-primary')
    ok.click()
    sleep(10)
    validation_code = browser.find_element_by_name('phone_code')
    code = input('Tapez le code reçu par sms: ')
    validation_code.send_keys(code + Keys.ENTER)
    return browser

def goToConversation(n=2):
    """n est est la postion de la discussion dans telegram"""
    global driver
    conversation_prestataire = driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div[2]/div/div/ul/li[{}]".format(str(n)))
    conversation_prestataire.click()

def sendMessage(msg):
    global driver
    message = driver.find_element_by_css_selector('.composer_rich_textarea')
    message.send_keys(msg + Keys.ENTER)

def readLatestMessage():
    global driver
    answers = driver.find_elements_by_css_selector('.im_message_text')
    text = answers[-1].get_attribute('innerHTML')
    return text

def computeAnswer(text):
    #que de faire une regex je fais cette petite acrobatie
    #j'étais en mode debug et je voulais pas importer une nouvelle lib :)
    numbers = text.replace("Vous avez 3 secondes pour valider l'operation ","").replace(" = ?","").split('*')
    return str(int(numbers[0])*int(numbers[1]))

#login 
driver = login()
#aller à la conversation avec prestataire
sleep(10)
goToConversation(2)
sleep(5)
#envoyer le message /contact au bot et attendre 0.5 secondes le temps qu'il réponde
sendMessage("/contact")
sleep(2)
#lire la dernière ligne du dernier message reçu 
text = readLatestMessage()
#extraire les deux nombre et calculer leur produit
ans = computeAnswer(text)
# répondre au bot
sendMessage(ans)
#Si tout va bien le flag devrait s'afficher
text = readLatestMessage()
print(text)
