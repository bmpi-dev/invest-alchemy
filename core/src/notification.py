import requests
import boto3
import json
import time
from constants import *

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

def send_sns(file_name):
    """Send message by sns
    Amazon SNS is designed to distribute notifications, If you wish to send formatted emails, consider using Amazon Simple Email Service (SES), which improves email deliverability.
    """
    subject = 'Double MA Strategy Trade Signal: ' + TODAY_STR + ' - A Share'
    with open(file_name, 'r') as file:
        message = file.read()
        sns_client = boto3.client('sns', region_name=AWS_REGION)
        sns_client.publish(
            TopicArn=SNS_TOPIC,
            Message=message,
            Subject=subject,
        )

def send_tg_msg(file_name):
    headers = {'Content-type': 'application/json'}
    subject = 'Double MA Strategy Trade Signal: ' + TODAY_STR + ' - A Share' + '\n\n'
    with open(file_name, 'r') as file:
        trad_msg = file.read()
    msg = subject + trad_msg
    for chat_id_name in TG_CHATS:
        chat_id, chat_name = chat_id_name.split(',')
        data = {'chat_id': chat_id, 'text': msg, 'parse_mode': 'HTML'}
        r = requests.post(TG_SEND_MESSAGE_API, data=json.dumps(data), headers=headers)
        if r.status_code != 200:
            print('Error sending message to TG chat ' + chat_name + '(' + chat_id + ')' + ': ' + str(r.text))

def send_email_smtp(to_address, subject, content):
    message = MIMEMultipart()
    message["From"] = formataddr((SMTP_MAIL_FROM_ALIAS, SMTP_MAIL_FROM))
    message["To"] = to_address
    message["Subject"] = subject
    
    message.attach(MIMEText(content, "plain"))

    with smtplib.SMTP(SMTP_ADDRESS, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.send_message(message)
        print(f'Email for {to_address} sent successfully!')

def send_emails_smtp(to_address_list, subject, content):
    to_address_list = list(set(to_address_list))

    try:
        sent_count = 0
        for to_address in to_address_list:
            send_email_smtp(to_address, subject, content)
            sent_count += 1
            if sent_count % SMTP_MAIL_RATE_LIMIT == 0:
                 time.sleep(1)
        print(f'{len(to_address_list)} emails sent successfully!')
    except Exception as e:
        print(e)
