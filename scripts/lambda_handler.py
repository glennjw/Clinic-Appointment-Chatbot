#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3
import json
import logging
import os
import aiml
import pymysql.cursors
import who_avai
import when_nurse
from base64 import b64decode
from urlparse import parse_qs


bot = aiml.Kernel()
bot.learn("taina.aiml")

connection = pymysql.connect(host='IP',
                             user='user',
                             password='pwd',
                             db='DB')
cursor = connection.cursor()




ENCRYPTED_EXPECTED_TOKEN = os.environ['kmsEncryptedToken']

kms = boto3.client('kms', region_name='us-east-1')
expected_token = kms.decrypt(CiphertextBlob=b64decode(ENCRYPTED_EXPECTED_TOKEN))['Plaintext']

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    params = parse_qs(event['body'])
    token = params['token'][0]
    if token != expected_token:
        logger.error("Request token (%s) does not match expected", token)
        return respond(Exception('Invalid request token'))
    
    user = params['user_name'][0]
    command = params['command'][0]
    channel = params['channel_name'][0]
    if 'text' in params:
        command_text = params['text'][0]
    else:
        command_text = ''
    
    return respond(None, "%s : %s" % (command_text, bot.respond(command_text)))
    

    
    
sentence = "What time is it?"
print(bot.respond(sentence))

sentence = "Who is available at 3 pm on Apr 26?"
print(bot.respond(sentence))

sentence = "What time is it?"
print(bot.respond(sentence))

sentence = "What time is it?"
print(bot.respond(sentence))

sentence = "What time is it?"
print(bot.respond(sentence))
