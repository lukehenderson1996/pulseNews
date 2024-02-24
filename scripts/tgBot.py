'''pulseNews telegram bot'''

# Author: Luke Henderson 
__version__ = '0.1'

import os
import time
import telebot
import re

import config as cfg
import apiKeys
import colors as cl
import debugTools as dt
import logger as lg
import utils as ut
import ytWrapper as ytw

cl.green('Program Start')

#--------------------------------------------------------------init--------------------------------------------------------------
#assert correct module versions 
modV = {cfg:  '0.4',
        cl:   '0.8',
        ytw:  '0.2'}
for module in modV:
    errMsg = f'Expecting version {modV[module]} of "{os.path.basename(module.__file__)}". Imported {module.__version__}'
    assert module.__version__ == modV[module], errMsg
    
bot = telebot.TeleBot(apiKeys.tgBotToken)


# @bot.message_handler(commands=['start', 'hello'])
# def send_welcome(message):
#     bot.reply_to(message, "Hello, world!")

# @bot.message_handler(func=lambda msg: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    userName = message.from_user.username or f"{message.from_user.first_name}_{message.from_user.id}"
    print(f"Incoming Message from {userName}: {message.text}")
    chatLogger = lg.LOGGER(['Time', 'Sender', 'Message'], 'chats/' , str(userName), persistent=True)
    chatLogger.simpLog([time.time(), 'user', message.text])
    
    response = "Hello, world!"
    chatLogger.simpLog([time.time(), 'assistant', response])
    bot.reply_to(message, response)
    
    print(f"Sent Message to {userName}: {response}")

@bot.message_handler(func=lambda message: 'youtube.com' in message.text or 'youtu.be' in message.text)
def send_summary(message):
    userName = message.from_user.username or f"{message.from_user.first_name}_{message.from_user.id}"
    cl.purple(f"Summarization command from {userName}: {message.text}")
    chatLogger = lg.LOGGER(['Time', 'Sender', 'Message'], 'chats/' , str(userName), persistent=True)
    chatLogger.simpLog([time.time(), 'user', message.text])
    
    vidID = None
    match = re.search(r'youtube\.com/watch\?v=([^&]+)', message.text) #https://www.youtube.com/watch?v=VIDEO_ID
    if match:
        vidID = match.group(1)
    match = re.search(r'youtu\.be/([^?/]+)', message.text) #https://youtu.be/VIDEO_ID
    if match:
        vidID = match.group(1)
    cl.yellow(f'Extracted video ID: {vidID}')

    if vidID:
        response = 'Summarizing...'
        chatLogger.simpLog([time.time(), 'assistant', response])
        bot.reply_to(message, response)
    
    if not vidID:
        response = f"Error: Couldn't extract YouTube video ID from message ({message.text})"
    else:
        response = ytw.summarize(vidID)

    MAX_MSG_LEN = 4096
    if len(response) > MAX_MSG_LEN:
        responseList = [response[i:i+MAX_MSG_LEN] for i in range(0, len(response), MAX_MSG_LEN)]
        for resp in responseList:
            chatLogger.simpLog([time.time(), 'assistant', resp])
            bot.reply_to(message, resp)
    else:
        chatLogger.simpLog([time.time(), 'assistant', response])
        bot.reply_to(message, response)
    
    print(f"Sent Message to {userName}:\n{response}\n---------Complete-------")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    userName = message.from_user.username or f"{message.from_user.first_name}_{message.from_user.id}"
    print(f"Incoming Message from {userName}: {message.text}")
    chatLogger = lg.LOGGER(['Time', 'Sender', 'Message'], 'chats/' , str(userName), persistent=True)
    chatLogger.simpLog([time.time(), 'user', message.text])
    
    response = f'Error: Unable to understand user input input "{message.text}"'
    chatLogger.simpLog([time.time(), 'assistant', response])
    bot.reply_to(message, response)
    
    print(f"Sent Message to {userName}: {response}")




#--------------------------------------------------------------main loop--------------------------------------------------------------
bot.infinity_polling()