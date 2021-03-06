# coding=utf-8
import logging
import os
from collections import Counter
from requests import ConnectionError

from wikiapi import WikiApi
from lxml import html
import requests
import smtplib
import urllib3
from twilio.rest import TwilioRestClient

logging.basicConfig(level=logging.DEBUG, filename='log.txt',format= '%(asctime)s - %(levelname)s - %(message)s',)

#urllib3.disable
logging.captureWarnings(True)
#
# wiki = WikiApi()
# wiki = WikiApi({ 'locale' : 'uk'})
# results = wiki.find('Thinkmobiles')
# article = wiki.get_article(results[0])
# print article.summary

#Список користувачів, яким дозволено редагувати статтю Thinkmobiles
my_list = ['Viktoria Rogachenko','Scamp68', 'Irina Grab', 'Юра Бисага']
#------------------------------------------------------------------
white_list = []
for x in my_list:
    white_list.append(x.decode('utf-8'))

#Дивимось в історії змін, хто і коли останній редагував статтю
try:
    page = requests.get('https://uk.wikipedia.org/w/index.php?title=ThinkMobiles&action=history',timeout=5)
    tree = html.fromstring(page.content)
    user_name = tree.xpath(".//*[@id='pagehistory']/li[1]/span[@class='history-user']/a//text()")
    time = tree.xpath(".//*[@id='pagehistory']/li[1]/a[@class='mw-changeslist-date']/text()")[0]
    last_modify = user_name[0]
    last_modify_time = time.split(',')[0]
except ConnectionError:
    print "Trouble with internet connection"
    logging.debug(u'Trouble with internet connection')
except IndexError:
    print "Problem with xpath"
    logging.debug(u'Problem with xpath')
#-------------------------------------------------------------
#Дивимось в історії змін, хто і коли останній редагував статтю в обговоренні
# page1 = requests.get('https://uk.wikipedia.org/w/index.php?title=%D0%9E%D0%B1%D0%B3%D0%BE%D0%B2%D0%BE%D1%80%D0%B5%D0%BD%D0%BD%D1%8F:ThinkMobiles&action=history',timeout=5)
# tree1 = html.fromstring(page1.content)
# user_name1 = tree1.xpath(".//*[@id='pagehistory']/li[1]/span[@class='history-user']/a//text()")
# time1 = tree1.xpath(".//*[@id='pagehistory']/li[1]/a[@class='mw-changeslist-date']/text()")[0]
# last_modify1 = user_name1[0]
# last_modify_time1 = time1.split(',')[0]
#-------------------------------------------------------------

try:

    if last_modify in white_list :
        logging.debug(u'Thinkmobiles wiki content was not changed')
        print "Ok"
    else:
        # if os.stat("log.txt").st_size == 0:
        #     print "File is empty"
        #     print "Email was send ............."
        #     print "User: " + last_modify + " Time: " + last_modify_time
        #     text_file = open("log.txt", "a")
        #     text_file.write(last_modify_time + " ddd5 " + last_modify + '\n')
        #     text_file.close()
        #
        # else:
        #
        #     text_file = open("log.txt", "rw")
        #     file_lists = text_file.readlines()
        #     penultimate = len(file_lists) - 2
        #     last = len(file_lists)
        #     two_last = file_lists[penultimate:last]
        #     text_file.close()
        #
        #     test1 = str(last_modify_time + " ddd5 " + last_modify+ '\n')
        #     test2 = file_lists[-1]
        #
        #
        #     if test1 == test2:
        #         print "ggg"
        #     else:
        #         print "fuck"
        #         print "User: " + last_modify + " Time: " + last_modify_time
        #         text_file = open("log.txt", "a")
        #         text_file.write(last_modify_time + " ddd5 " + last_modify + '\n')
        #         text_file.close()
        #
        #
        #     try:
        #         text_file = open("log.txt", "rw")
        #         file_lists = text_file.readlines()
        #         penultimate = len(file_lists) - 2
        #         last = len(file_lists)
        #         two_last = file_lists[penultimate:last]
        #         text_file.close()
        #         a = two_last[0]
        #         b = two_last[1]
        #         if a == b:
        #             print "Povtor"
        #         else:
        #
        #             print "User: " + last_modify + " Time: " + last_modify_time
        #             print "Email was send ............."
        #
        #     except IndexError:
        #         print "User: " + last_modify + " Time: " + last_modify_time
        #         text_file = open("log.txt", "a")
        #         text_file.write(last_modify_time + " ddd5 " + last_modify + '\n')
        #         text_file.close()
        #         print "Email was send ............."
        #         print "txt file contain only one line"







        account_sid = "AC707e9ab0c1b55f8259e6d4e9738fc9ba"
        auth_token = "6809c444a4d05a9f018c43bc40d5f823"
        client = TwilioRestClient(account_sid, auth_token)

        message = client.messages.create(to="+380957089129", from_="+12562700265",
                                             body= "Something has been changed in wikipedia.")
        logging.debug(u'SMS was sent on +380957089129')
        server = smtplib.SMTP('smtp.gmail.com:587')
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login("scamp68@gmail.com", "Seatao5803axleon87")
        server_ssl.sendmail("scamp68@gmail.com", "oleg.stasiv@thinkmobiles.com", "Something has been changed in wikipedia.")
        server_ssl.close()
        logging.debug(u'Email was sent to oleg.stasiv@thinkmobiles.com')
except Exception, e:
    print "Error"
