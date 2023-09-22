#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import imaplib
import email
import json
import os

with open('config.json', 'r') as f_config:
    config = json.load(f_config)

mail = imaplib.IMAP4_SSL('imap.gmail.com', port=993)
mail.login(config["LOGIN"], config["PASSWORD"])
mail.list()
mail.select("inbox")

# result, data = mail.search(None, 'FROM', '"platform@21-school.ru"', '(HEADER Subject "Someone registered for a project review")')
result, data = mail.search(None, '(HEADER Subject "Someone registered for a project review")')

# result, data = mail.search(None, "ALL")
 
ids = data[0]
id_list = ids.split()

dictionary = {}

i = 6
while i > 1:
    i -= 1
    num = 0-i
    latest_email_id = id_list[num]
    result, data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    dictionary.update({email_message['Date']:email_message['Subject']})
print(dictionary)
json_in_file = json.dumps(dictionary)
os.remove("output.txt")
print(json_in_file, file=open('output.txt', 'a'))
print(dictionary["Sat, 17 Jun 2023 03:20:38 -0700 (PDT)"])