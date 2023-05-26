'''Twitter scraping tools'''
#https://github.com/shaikhsajid1111/twitter-scraper-selenium

# Author: Luke Henderson
__version__ = '0.1'

import twitter_scraper_selenium  as twss

import colors as cl
import debugTools as dt
import utils as ut

class Scraper:
    '''Scraper class'''

    def __init__(self, headless=True):
        '''Short description\n
        Args:
            headless [bool, optional]: Whether to display nothing, or the web browser'''
        self.headless = headless
    
    def run(self, usr, count=3):
        return twss.scrape_profile(twitter_username=usr, output_format="json",
                            browser="chrome", tweets_count=count)


if __name__ == '__main__':
    cl.green('Program Start')
    tScraper = Scraper()
    tweets = tScraper.run('stkirsch')
    dt.info(tweets, 'tweets')
