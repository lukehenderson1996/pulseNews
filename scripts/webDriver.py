'''Headless (or not) browser tools'''

# Author: Luke Henderson and Dawson Fields
__version__ = '0.2'

import selenium as sl
from selenium.webdriver.common.by import By as slBy
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import json
import xmltodict
import requests

import colors as cl
import debugTools as dt
import utils as ut

class SeleniumChromeBrowser:
    '''SeleniumChromeBrowser class'''

    def __init__(self, headless=True):
        '''Automated web browsing with Selenium driving Chrome\n
        Args:
            headless [bool, optional]: Whether to display nothing, or the web browser'''
        self.options = sl.webdriver.ChromeOptions()
        if headless:
            self.options.add_argument("--headless=new")
        self.options.add_argument("--enable-features=UseOzonePlatform")
        self.options.add_argument("--ozone-platform=wayland")
        # self.options.add_argument('--log-level=3')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])

    def findYtRss(self, url):
        '''Short description'''
        with sl.webdriver.Chrome(service=ChromeService(ChromeDriverManager(log_level=3).install()), options=self.options) as driver:
            driver.get(url)
            chanUrl = driver.current_url
            chanRss = driver.find_element(by= slBy.XPATH, value="//*[@title='RSS']").get_attribute('href')
            print("Channel URL:", chanUrl)
            print("Channel RSS:", chanRss)
            driver.close()
        return chanRss

    def pullRss(self, rssFeedUrl):
        data_dict = xmltodict.parse(requests.get(rssFeedUrl).content)
        json_data = json.dumps(data_dict)
        return data_dict
    
    def loadPage(self, url):
        with sl.webdriver.Chrome(service=ChromeService(ChromeDriverManager(log_level=3).install()), options=self.options) as driver:
            driver.get(url)
            ut.pause()


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

    # #twitter attempt
    # url = 'https://twitter.com/stkirsch'
    # webDriver = SeleniumChromeBrowser(headless=False)
    # webDriver.loadPage(url)