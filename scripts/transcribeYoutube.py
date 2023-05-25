"""Youtube transcriptions"""

# Authors: Luke Henderson and Dawson Fields 
__version__ = '0.1'

import os
from youtube_transcript_api import YouTubeTranscriptApi

import colors as cl
import debugTools as dt



class YoutubeTranscriber:
    """Short description"""

    def __init__(self, vidId, shouldPrint=False):
        """Short description\n
        Args:
            arg1 [str]: description\n
        Return:
            [int] 0 for pass
        Notes:
            notes here"""
        #internal automatically called init code here
        self.vidId = vidId
        self.shouldPrint = shouldPrint

    def run(self):
        resp = YouTubeTranscriptApi.get_transcript(self.vidId)

        # dt.info(resp, 'resp')

        allText = ''
        for item in resp:
            allText = allText + item['text'].replace('\n', ' ')

        if self.shouldPrint: 
            dt.info(allText, 'allText')
            dt.info(len(allText.split(' ')), 'test')

        return allText


if __name__ == '__main__':
    pass