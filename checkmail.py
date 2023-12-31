#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import imaplib
import email
import json
import os
import requests

absolute_path = os.path.dirname(__file__)
file_cfg = absolute_path + "/" + "config.json"
file_info = absolute_path + "/" + "mail.info"


with open(file_cfg, 'r') as f_config:
    config = json.load(f_config)

subj = "(HEADER Subject \"" + config["SUBJECT"] + "\")"

mail = imaplib.IMAP4_SSL('imap.gmail.com', port=993)
mail.login(config["LOGIN"], config["PASSWORD"])
mail.list()
mail.select(config["MAIL_FOLDER"])

# result, data = mail.search(None, 'FROM', '"platform@21-school.ru"', '(HEADER Subject "Someone registered for a project review")')
result, data = mail.search(None, subj)


ids = data[0]
id_list = ids.split()

with open(file_info, 'r') as dic_f:
    dic = json.load(dic_f)

i = config["MAIL_COUNT"]
count_new = 0
while i > 0:
    i -= 1
    num = 0-i
    latest_email_id = id_list[num]
    result, data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    if email_message['Date'] not in dic:
        count_new = count_new + 1
        dic.update({email_message['Date']:email_message['Subject']})
mail.logout()
json_in_file = json.dumps(dic)
os.remove(file_info)
print(json_in_file, file=open(file_info, 'a'))

# Send new message count in Telegram
# https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=<MSG_TEXT>

if count_new > 0:
    msg_text = "Новые записи на проверки: " + str(count_new)
    url = "https://api.telegram.org/bot" + config["tgToken"] + "/sendMessage?chat_id=" + config["tgUserID"] + "&text=" + msg_text
    requests.post(url)
    msg_text = "https://edu.21-school.ru/"
    url = "https://api.telegram.org/bot" + config["tgToken"] + "/sendMessage?chat_id=" + config["tgUserID"] + "&text=" + msg_text
    requests.post(url)
    msg_text = "📍ПРОВЕРЬ КАЛЕНДАРЬ📍"
    url = "https://api.telegram.org/bot" + config["tgToken"] + "/sendMessage?chat_id=" + config["tgUserID"] + "&text=" + msg_text
    requests.post(url)

