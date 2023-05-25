'''Headless (or not) browser tools'''

# Author: Luke Henderson and Dawson Fields
__version__ = '0.2'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import json
import xmltodict
import requests

import colors as cl
import debugTools as dt

class SeleniumChromeBrowser: #or, ClassName
    '''SeleniumChromeBrowser class'''
    internalConstant = 2e-6

    def __init__(self, headless=True):
        '''Short description\n
        Args:
            arg1 [str]: description\n
            arg2 [float]: description\n
            optionalArg3 [str, optional]: 
                long description------------------------
        Return:
            [int] 0 for pass
        Notes:
            notes here'''
        self.internalVariable = 'variable content'
        
        self.options = webdriver.ChromeOptions()
        if headless:
            self.options.add_argument("--headless=new")
        self.options.add_argument("--enable-features=UseOzonePlatform")
        self.options.add_argument("--ozone-platform=wayland")
        self.options.add_argument('--log-level=3')

    def findYtRss(self, url):
        '''Short description'''
        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options) as driver:
            driver.get(url)

            chanUrl = driver.current_url
            chanRss = driver.find_element(by= By.XPATH, value="//*[@title='RSS']").get_attribute('href')
            print("Channel URL:", chanUrl)
            print("Channel RSS:", chanRss)

        return chanRss

    def pullRss(self, rssFeedUrl):
        data_dict = xmltodict.parse(requests.get(rssFeedUrl).content)
        json_data = json.dumps(data_dict)

        return data_dict


if __name__ == '__main__':
    cl.green('Program Start')
    # #get RSS URL
    # url = "https://www.youtube.com/@TimcastNews"
    # webDriver = SeleniumChromeBrowser(headless=False)
    # chanRss = webDriver.findYtRss(url)

    #get json data from RSS feed
    url = 'https://www.youtube.com/feeds/videos.xml?channel_id=UCe02lGcO-ahAURWuxAJnjdA'
    webDriver = SeleniumChromeBrowser(headless=False)
    feed = webDriver.pullRss(url)
    dt.info(feed, 'feed')