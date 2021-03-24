#!/usr/bin/env python
"""created on 2021-03-23"""

import argparse
import json
import os
import pathlib
import ssl
import time

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from markdown import Markdown
from smtplib import SMTP


import csv
import datetime
from collections import defaultdict


def get_birthday_messages():
    birthdays = defaultdict(list)
    file = os.getenv('BIRTHDAYS_CSV')
    file = file.replace('\\n','\n')
    csv_reader = csv.DictReader(file.splitlines())
    for line in csv_reader:
        persons_real_birthday = line.values()
        birthday_as_month_day = datetime.datetime.strptime(line["day"], "%Y-%m-%d").strftime("%m-%d")
        birthdays[birthday_as_month_day].append(persons_real_birthday)

    today = datetime.date.today()
    calc_age = lambda born: today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    todays_birthdays = birthdays[today.strftime("%m-%d")]
    birthday_messages = []
    for real_birthday, name in todays_birthdays:
        age_today = calc_age(datetime.datetime.strptime(real_birthday, "%Y-%m-%d"))
        if age_today > 1:
            birthday_message = f"* {name} turned {age_today} today!"
        else:
            birthday_message = f"* {name} has a birthday today!"
        birthday_messages.append(birthday_message)
    return birthday_messages

def main():
    password = os.getenv('EMAIL_HOST_PASSWORD')
    host = os.getenv('EMAIL_HOST')
    from_email = os.getenv('EMAIL_HOST_USER')
    to_email = os.getenv('EMAIL_TO')
    csv_string = os.getenv('BIRTHDAYS_CSV')
    error_msg = 'Please add BIRTHDAYS_CSV, EMAIL_HOST_PASSWORD, EMAIL_HOST, EMAIL_HOST_USER, and EMAIL_TO as env vars'
    assert all([birthdays_csv, password, host, from_email, to_email]), error_msg

    birthday_messages = get_birthday_messages()
    if not birthday_messages:
        print(f'no birthdays today :) {datetime.datetime.now()}')
        return

    message = MIMEMultipart("alternative")
    message["Subject"] = f"{datetime.date.today()} Birthdays Reminder"
    message["From"] = from_email
    message["To"] = to_email

    markdowner = Markdown()
    text = "\n".join(birthday_messages)
    html = markdowner.convert(text)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with SMTP(host=host, port=587) as server:
        server.starttls(context=context)
        server.login(from_email, password)
        server.sendmail(from_email, to_email, message.as_string())
        print(f'sent email at {datetime.datetime.now()}')


if __name__ == "__main__":
    main()

