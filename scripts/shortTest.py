'''Place to test short code'''

# Author: Luke Henderson

import os
import time
from datetime import datetime

import colors as cl
import debugTools as dt
import logger as lg
import utils as ut

cl.green('Program Start')
progStart = time.time()




myStr = '1234567890abcde'

chatLogger = lg.LOGGER(['Time', 'Sender', 'Message'], 'chats/' , str(None), persistent=True)
chatLogger.simpLog(['','',''])