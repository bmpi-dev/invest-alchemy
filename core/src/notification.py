import requests
import boto3
import json
from constants import TODAY_STR, SNS_TOPIC, AWS_REGION, TG_SEND_MESSAGE_API, TG_CHATS

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
