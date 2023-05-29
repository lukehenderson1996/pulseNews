'''Youtube transcriptions and rss information gathering tools'''

# Authors: Luke Henderson and Dawson Fields 
__version__ = '0.21'

import os
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup

import colors as cl
import debugTools as dt
import api


class YoutubeTranscriber:
    '''YoutubeTranscriber class'''

    def __init__(self, vidId, shouldPrint=False):
        '''Short description\n
        Args:
            arg1 [str]: description\n
        Return:
            [int] 0 for pass
        Notes:
            notes here'''
        self.vidId = vidId
        self.shouldPrint = shouldPrint

    def run(self):
        resp = YouTubeTranscriptApi.get_transcript(self.vidId)

        # dt.info(resp, 'resp')

        allText = ''
        for item in resp:
            allText = allText + item['text'].replace('\n', ' ') + ' '

        if self.shouldPrint: 
            dt.info(allText, 'allText')
            dt.info(len(allText.split(' ')), 'test')

        return allText



if __name__ == '__main__':
    cl.green("Program Start")
    URL = "https://www.youtube.com/@TimcastNews"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    # rssTitle = soup.find_All('div')
    print(soup.title)
    for a in soup.find_all('link', href=True):
        print("Found the URL:", a['href'])
    # dt.info(page.content)


