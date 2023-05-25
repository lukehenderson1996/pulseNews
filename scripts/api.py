'''REST API manager'''

# Author: Luke Henderson
__version__ = '0.5'

import json
import requests
import time
from datetime import datetime

import debugTools as dt
import colors as cl
import logger as lg
import utils as ut

def infRetry(url, method='GET', headers=None, body=None, timeout=5, retryDelay=3, knownErrors=[]):
    '''Wrapper to retry getResp repeatedly\n
        Args:
            url [str]: url to GET
            timeout [float]: client timeout
        Return:
            responseJSON [JSON object]: response from API'''
    while True:
        responseJSON = getResp(url, method=method, headers=headers, body=body, timeout=timeout, knownErrors=knownErrors)
        if responseJSON != None:
            return responseJSON
            # if responseJSON == 'api.py Error: assume prev success':
            #     return responseJSON
            # else:
            #     return responseJSON
        time.sleep(retryDelay)
    # responseJSON = None
    # while responseJSON == None:
    #     responseJSON = getResp(url, timeout=timeout)
    #     if responseJSON == None:
    #         time.sleep(retryDelay)
    # return responseJSON

def getResp(url, method='GET', headers=None, body=None, timeout=5, knownErrors=[]):
    '''Short description\n
        Args:
            url [str]: url to GET
            timeout [float]: client timeout
        Return:
            responseJSON [JSON object]: response from API'''
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=timeout)
        elif method == 'POST':
            assert body != None
            response = requests.post(url, headers=headers, data=body, timeout=timeout)
        else:
            cl.red(f'Error (api.py): Method "{method}" not supported')
            raise Exception(f'Unsupported call method "{method}" for api.py') 
    except requests.exceptions.ConnectionError:
        cl.red('API error handler: connection error')
        return None
    except requests.exceptions.Timeout:
        cl.red('API error handler: timeout')
        return None
    if response.status_code != 200:
        currTime = time.time()
        dateObj = datetime.fromtimestamp(currTime)
        humReadDate, humReadTime = ut.humTime()
        cl.red(f'Start api.py error handler: {humReadDate} {humReadTime}')

        for knownError in knownErrors:
            if response.status_code == knownError['status_code']:
                urlMatch = False
                if url == knownError['url']:
                    #url exact match
                    urlMatch = True
                elif 'urlMatch' in knownError and knownError['urlMatch']=='prefix':
                    #url not exact match, but matching prefix is OK
                    strLen = len(knownError['url'])
                    if url[:strLen] == knownError['url']:
                        urlMatch = True
                if urlMatch:
                    #start known error handling
                    if knownError['decision'] == 'sleep and retry':
                        #sleep and retry
                        cl.yellow(f'Known error {response.status_code} for url: \n{url}')
                        sleepTime = knownError['sleepTime']
                        cl.yellow(f'Sleeping for {sleepTime} second(s), then resuming')
                        time.sleep(sleepTime)
                        return None
                    elif knownError['decision'] == 'retry':
                        #retry
                        cl.yellow(f'Known error {response.status_code}. Decision: immediate retry. url: \n{url}')
                        return None
                    elif knownError['decision'] == 'assume prev success':
                        respJSON = response.json()
                        if len(respJSON['errors']) > 1:
                            cl.red('Error (api.py): More than one error in respJSON')
                            dt.info(respJSON, 'respJSON')
                            exit()
                        elif respJSON['errors'][0]['code'] == 2002:
                            cl.yellow(f'Known error {response.status_code}. Decision: assume prev success. url: \n{url}')
                            return 'api.py Error: assume prev success'
                        else:
                            cl.red('Error (api.py): Unrecognized JSON error code')
                            dt.info(response, 'response')
                            dt.info(respJSON, 'respJSON')
                            exit()
                    else:
                        #unknown decision
                        cl.red(f'Error (api.py): given unrecognized decision {knownError["decision"]}')
                        dt.info(knownError, 'knownError')
                        exit()
                    
                    

        myLog = lg.LOGGER(logCols=['Time', 'url', 'status_code', 'reason' 'text', 'content'], xml=True, quiet=False)
        myLog.simpLog([currTime, response.url, response.status_code, response.reason, response.text, str(response.content)])


        dt.info(response, 'response')
        cl.red(f'End api.py error handler: Failed to retrieve data from API, response code {response.status_code}')

        myLog.close()
        raise Exception
    return response.json()











