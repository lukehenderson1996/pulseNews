'''pulseNews'''

# Authors: Luke Henderson and Dawson Fields 
__version__ = '0.4'

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
        cl.red('Error (main.py): Model stopped with incorrect finish reason: ' + reason)

def printPrice(resp, model):
    if model in MODEL_PRICES:
        cl.yellow(f'Cost: ${MODEL_PRICES[model]}*{resp["usage"]["total_tokens"]}/1000 = ' +
                  f'{MODEL_PRICES[model]*resp["usage"]["total_tokens"]/10}¢')
    else:
        cl.red('Error (main.py): Other model costs not defined')

def costStr(resp, model):
    ret = cl.WARNING
    if model in MODEL_PRICES:
        ret += f'{round(MODEL_PRICES[model]*resp["usage"]["total_tokens"]/10, 4)}¢'
    else:
        cl.red('Error (main.py): Other model costs not defined')
    return ret

cl.green('Program Start')

#--------------------------------------------------------------init--------------------------------------------------------------
#assert correct module versions 
modV = {cfg:  '0.3',
        cl:   '0.8',
        api:  '0.5'}
for module in modV:
    errMsg = f'Expecting version {modV[module]} of "{os.path.basename(module.__file__)}". Imported {module.__version__}'
    assert module.__version__ == modV[module], errMsg
#init openai
openai.api_key = apiKeys.openaiPriv
#warn if using paid API calls
if cfg.simulateCompletions:
    cl.yellow('Using simulated completions')
else:
    input(f'{cl.WARNING}Warning: main.py using paid API calls. Press enter to continue...{cl.ENDC}')
# #list models available
# openListResp = openai.Model.list()
# # dt.info(openListResp)
# modelList = openListResp['data']
# for model in modelList:
#     print(model['id'])




#------------------------------------------------------main loop------------------------------------------------------

#----------------------------------------------------ytTranscribe----------------------------------------------------
if 'ytTranscribe' in cfg.jobs:
    #init youtube transcriber
    ytTranscriber = tranYt.YoutubeTranscriber(cfg.vidId, shouldPrint=False)
    #youtube transcription GET
    cl.blue(f'Getting transcription for video ID "{ytTranscriber.vidId}"')
    videoText = ytTranscriber.run()

    #openai summarization
    model = "gpt-3.5-turbo"
    cl.blue(f'Summarizing content using LLM "{model}"')
    prompt = ''
    if cfg.simulateCompletions:
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
        wordCount = len(videoText.split(" "))
        print(f'Word count: {wordCount}')
        if wordCount > 2500:
            videoTextLen = len(videoText)
            abrigedLen = int((2500/wordCount)*videoTextLen)
            videoText = videoText[:abrigedLen]
            wordCount = len(videoText.split(" "))
            cl.blue(f'Abridging video transcript for a new word count of {wordCount}')
        compResp = openai.ChatCompletion.create(
            model=model, 
            temperature=0, 
            max_tokens=350, 
            top_p=1,
            messages=[
                {"role": "system", "content": "You are an Analyst for a corporate intelligence group. You generate concise bullet points (no more than 4 bullet points) of input information for the company to later aggregate and analyze. You don't perform any analysis on the input content. You merely summarize it in bullet point (no more than 4 bullet points) format in the voice of the original author. "},
                {"role": "user", "content": videoText} 
            ] 
        )

    # dt.info(compResp, 'compResp')
    cost = costStr(compResp, model)
    cl.blue(f'\nResponse from {compResp["model"]}:\t\t' + cost)
    checkFinish(compResp)

    cl.blue('Response digested: ')
    cont = compResp['choices'][0]['message']['content']
    print(f'Content is: \n{cont}')


#----------------------------------------------------tweetAnalysis----------------------------------------------------
if 'tweetAnalysis' in cfg.jobs:
    #pull latest tweets from account
    twAccount = 'Jikkyleaks'
    tweetResp = {'tweet 1': None, 'tweet 2': None, 'tweet 3': None, 'tweet 4': None, 'tweet 5': None}
    tweetResp['tweet 1'] = "\nHe actually said...\n\"Woman is a social construct\"\n\nI'm getting out of the way.\n#justsayin\n"
    tweetResp['tweet 2'] = "\nJikkyleaks 🐭 Retweeted\nBroken Truth\n@BrokenTruthTV\n·\n2h\n\"Vaccine enhancement\" you say? This is why they kept Francis Collins away from the cameras.\n"
    tweetResp['tweet 3'] = "\nJikkyleaks 🐭 Retweeted\nJurassic Carl 🦖🐭\n@carl_jurassic\n·\n3h\nReplying to \n@masterlongevity\n and \n@Jikkyleaks\n“Master longevity”\n\nAdd to the list of anti aging gurus who jibber jab for the Jibby jab!\n"
    tweetResp['tweet 4'] = "\nCringe tweet of the week\n"
    tweetResp['tweet 5'] = "\n🚨 26.4% excess deaths in the 0-24 age bracket!! \n\nWake up, everyone! \n\nThese are kids!\n"


    model = "text-davinci-003"
    # prompt = "How important are these tweets on a scale of 1-10?\n\n<tweet 1>\nHe actually said...\n\"Woman is a social construct\"\n\nI'm getting out of the way.\n#justsayin\n</tweet 1>\n<tweet 2>\nJikkyleaks 🐭 Retweeted\nBroken Truth\n@BrokenTruthTV\n·\n2h\n\"Vaccine enhancement\" you say? This is why they kept Francis Collins away from the cameras.\n</tweet 2>\n<tweet 3>\nJikkyleaks 🐭 Retweeted\nJurassic Carl 🦖🐭\n@carl_jurassic\n·\n3h\nReplying to \n@masterlongevity\n and \n@Jikkyleaks\n“Master longevity”\n\nAdd to the list of anti aging gurus who jibber jab for the Jibby jab!\n</tweet 3>\n<tweet 4>\nCringe tweet of the week\n</tweet 4>\n<tweet 5>\n🚨 26.4% excess deaths in the 0-24 age bracket!! \n\nWake up, everyone! \n\nThese are kids!\n</tweet 5>\nFormat:\n{'tweet 1': x, 'tweet 2': x, 'tweet 3': x,  'tweet 4': x, 'tweet 5': x}\n\n{'tweet 1': 3, 'tweet 2': 6, 'tweet 3': 4,  'tweet 4': 1, 'tweet 5': 10}/n/n{"
    prompt = "How important are these tweets on a scale of 1-10?\n\n" + \
                        "<tweet 1>" + tweetResp['tweet 1'] + \
            "</tweet 1>\n<tweet 2>" + tweetResp['tweet 2'] + \
            "</tweet 2>\n<tweet 3>" + tweetResp['tweet 3'] + \
            "</tweet 3>\n<tweet 4>" + tweetResp['tweet 4'] + \
            "</tweet 4>\n<tweet 5>" + tweetResp['tweet 5'] + \
            "</tweet 5>\nFormat:\n{'tweet 1': x, 'tweet 2': x, 'tweet 3': x,  'tweet 4': x, 'tweet 5': x}\n\n{"
    if cfg.simulateCompletions:
        compResp = {'id': 'cmpl-7GIqPtDF3cFJVvTaFkBTPP8o7izcV', 'object': 'text_completion', 'created': 1684120041, 'model': 'text-davinci-003', 'choices': [{'text': "'tweet 1': 3, 'tweet 2': 6, 'tweet 3': 4,  'tweet 4': 1, 'tweet 5': 10", 'index': 0, 'logprobs': None, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 360, 'completion_tokens': 35, 'total_tokens': 395}}
    else:
        compResp = openai.Completion.create(model=model, prompt=prompt, temperature=0, max_tokens=100,
            top_p=1, frequency_penalty=0, presence_penalty=0, stop=["}"])

    # dt.info(compResp, 'compResp')

    cost = costStr(compResp, model)
    cl.blue(f'\nResponse from {compResp["model"]}:\t\t' + cost)
    checkFinish(compResp)
    #convert response (with error detection)
    try:
        impDict = ast.literal_eval('{' + compResp['choices'][0]['text'] + '}')
        assert isinstance(impDict, dict)
        assert len(impDict)==5
        keyList = [str(key) for key in impDict.keys()]
        for i in range(len(impDict)):
            assert keyList[i] == f'tweet {i+1}'
            value = impDict[keyList[i]]
            assert isinstance(value, int)
            assert value >= 1
            assert value <= 10
    except AssertionError:
        cl.red('Error (main.py): Response from model in wrong format')
        dt.info(impDict, 'impDict')
        exit()
    print('Importance ratings: ')
    for key, value in impDict.items():
        print(f'\t{key}: {value}')



    #summarize important tweets:
    sortedImpDict = sorted(impDict.items(), key=lambda x: x[1], reverse=True)
    tweetList = []
    tweetList.append(sortedImpDict[0][0]) #most important tweet
    tweetList.append(sortedImpDict[1][0]) #second most important tweet

    model = "text-davinci-003"

    sumList = []
    for i in range(2):
        prompt = "Summarize this tweet in half the words or less\n\n<tweet>" + tweetResp[tweetList[i]] + "</tweet>"
        if cfg.simulateCompletions:
            sumList.append({'id': 'cmpl-7GKXMxBe5cxWeXjOzHliMp1W0KVIZ', 'object': 'text_completion', 'created': 1684126548, 'model': 'text-davinci-003', 'choices': [{'text': "Excess deaths in 0-24 age group; urgent call.", 'index': 0, 'logprobs': None, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 56, 'completion_tokens': 14, 'total_tokens': 70}})
        else:
            sumList.append(openai.Completion.create(model=model, prompt=prompt, temperature=1, max_tokens=25,
                top_p=1, frequency_penalty=0, presence_penalty=0))

    cl.purple('\nTweet Analysis Report: \n')
    for i in range(2):
        cost = costStr(sumList[i], model)
        cl.blue(f'1: {twAccount} tweet summary from {sumList[i]["model"]}:\t\t' + cost)
        checkFinish(sumList[i])
        text = sumList[i]['choices'][0]['text'].strip('\n')
        print(text + '\n')







#----------------------------------------------------testLogger----------------------------------------------------
if 'testLogger' in cfg.jobs:
    #save example relevant channel data
    chId = '@TimcastNews'
    chUrl = "https://www.youtube.com/@TimcastNews"
    chRss = 'https://www.youtube.com/feeds/videos.xml?channel_id=UCe02lGcO-ahAURWuxAJnjdA'
    
    xmlLog = lg.LOGGER(logCols=['chId', 'chUrl', 'chRss'], 
                       prefix='test logs/', filename='channel info', xml=True, quiet=False)
    xmlLog.simpLog([chId,chUrl,chRss])

    #pull saved channel data from long term memory into dict
    with open(ut.pth('/datalogs/test logs/channel info.xml', 'rel1'), 'r') as chInfo:
        chInfoDict = xmltodict.parse(chInfo.read())
        chInfoDict = chInfoDict['root']
    dt.info(chInfoDict, 'chInfoDict')