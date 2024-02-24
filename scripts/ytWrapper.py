'''YouTube wrapper for telegram bot'''

# Authors: Luke Henderson  
__version__ = '0.2'

import time
import os
import sys
import openai
import ast
import xmltodict

import config as cfg
import apiKeys
import colors as cl
import debugTools as dt
import logger as lg
import utils as ut
import api
import transcribeYoutube as tranYt


#constants:
#https://openai.com/pricing
MODEL_PRICES = {'text-davinci-003': 0.02, 'text-curie-001': 0.002, 'text-babbage-001': 0.0005, 'text-ada-001': 0.0004,
                'gpt-3.5-turbo': 0.002} #$/1k tokens
TOKEN_MAXES = {'text-davinci-003': 0, 'text-curie-001': 0, 'text-babbage-001': 0, 'text-ada-001': 0,
                'gpt-3.5-turbo': 4097} #????? need to find info per model

def checkFinish(resp):
    reason = resp["choices"][0]["finish_reason"]
    if reason != 'stop':
        cl.red('Error (ytWrapper.py): Model stopped with incorrect finish reason: ' + reason)

# def printPrice(resp, model):
#     if model in MODEL_PRICES:
#         cl.yellow(f'Cost: ${MODEL_PRICES[model]}*{resp["usage"]["total_tokens"]}/1000 = ' +
#                   f'{MODEL_PRICES[model]*resp["usage"]["total_tokens"]/10}¢')
#     else:
#         cl.red('Error (ytWrapper.py): Other model costs not defined')

def costStr(resp, model):
    # ret = cl.WARNING
    ret = ''
    if model in MODEL_PRICES:
        ret += f'{round(MODEL_PRICES[model]*resp["usage"]["total_tokens"]/10, 4)}¢'
    else:
        cl.red(f'Error (ytWrapper.py): This model ({model}) cost not defined')
    # ret += cl.ENDC
    return ret

def summarize(vidID):
    #init
    openai.api_key = apiKeys.openaiPriv
    ret = ''

    #init youtube transcriber
    ytTranscriber = tranYt.YoutubeTranscriber(vidID, shouldPrint=False)
    #youtube transcription GET
    ret += f'Fetching transcription for video ID "{ytTranscriber.vidId}"\n'
    videoText = ytTranscriber.run()
    ret += f'Content length is {len(videoText)}\n\n'

    #openai summarization
    model = "gpt-3.5-turbo"
    ret += f'Summarizing content using LLM "{model}"\n'
    prompt = ''
    if cfg.tgSimulateCompletions:
        compResp = {
            "id": "chatcmpl-7JwIDDHYhtwuySIlsIgik8nwjF41t",
            "object": "chat.completion",
            "created": 1684986665,
            "model": "gpt-3.5-turbo-0301",
            "usage": {
                "prompt_tokens": 3106,
                "completion_tokens": 98,
                "total_tokens": 3204
            },
            "choices": [
                {
                "message": {
                    "role": "assistant",
                    "content": "- Smartphone cameras have evolved from simple sensors to complex computational systems that rely heavily on software.\n- Google's Pixel camera system has been successful due to its consistent use of the same sensor and software tuning combo.\n- Apple's iPhone 14 Pro's new 48-megapixel sensor has resulted in some overprocessed photos, but software updates are expected to improve this.\n- Skin tone representation is a significant factor in photo comparisons between smartphones, with Google's Real Tone technology being a standout feature."
                },
                "finish_reason": "stop",
                "index": 0
                }
            ]
        }

        # print(compResp["choices"][0]["message"]["content"])
    else:
        ret += '\n'
        textJobs = []
        wordCountList = []
        wordCount = len(videoText.split(" "))
        i = 0
        runFlag = True
        while runFlag:
            videoTextLen = len(videoText)
            abrigedLen = int((2500/wordCount)*videoTextLen)
            # print(f'is {len(videoText)} greater than {abrigedLen}?')
            if len(videoText) > abrigedLen:
                textJobs.append(videoText[:abrigedLen])
                videoText = videoText[abrigedLen-2:]
            else:
                textJobs.append(videoText)
                videoText = ''
                runFlag = False
            wordCount = len(videoText.split(" "))
            wordCountList.append(wordCount)
            # dt.info(textJobs, 'textJobs')
            # cl.yellow(f'len of textJob[0] = {}')
            wordCountThisJob = len(textJobs[i].split(" "))

            i += 1
            ret += f'Job {i} created with word count of {wordCountThisJob}\n'


        i = 0
        for job in textJobs:
            # cl.blue(f'\nRunning job {i+1}...')
            # userInput = input("Press enter to continue, or type n to skip ")
            # if userInput == 'n':
            #     cl.yellow('skipping...')
            #     i += 1
            #     continue

            #system message #1: has a bug where sometimes the LLM will not summarize in bullet points
            # systemMessage = f"You are an Analyst for a corporate intelligence group. You generate concise bullet points (no more than {cfg.tgBulletPointNum} bullet points) of input information for the company to later aggregate and analyze. You don't perform any analysis on the input content. You merely summarize it in bullet point format in the voice of the original author. "
            #system message #2
            systemMessage = f"You are an Analyst for a corporate intelligence group. You generate concise bullet points (no more than {cfg.tgBulletPointNum} bullet points) of input information for the company to later aggregate and analyze. You don't perform any analysis on the input content. You merely summarize it in bullet point format with the same intent as the original author. \n\n Example output:\n-First bullet point summarizing first bit of information\n-Second bullet point summarizing the second bit of information\n-Third bullet point summarizing the third bit of information\netc..."
            compResp = openai.ChatCompletion.create(
                model=model, 
                temperature=0, 
                max_tokens=int(cfg.tgBulletPointNum*cfg.tgTokensPerbp), 
                top_p=1,
                messages=[
                    {"role": "system", "content": systemMessage},
                    {"role": "user", "content": job} 
                ] 
            )
            # dt.info(compResp, 'compResp')
            cost = costStr(compResp, model)
            ret += f'\nResponse {i+1} from {compResp["model"]}:\t\t' + cost + '\n'
            checkFinish(compResp)

            cont = compResp['choices'][0]['message']['content']
            ret += f'{cont}\n'

            i += 1
    return ret

