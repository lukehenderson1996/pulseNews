'''config.py: config constants for pulseNews'''

# Author: Luke Henderson
__version__ = '0.3'

#run/debug mode settings
jobs = [] #list of jobs to run. Options are: ['ytTranscribe', 'pullRss', 'tweetAnalysis', 'testLogger']
logEn = False
#data sim
simulatedData = True #quickly runs without paying for API calls (simulated openai completions)

#youtube video to transcribe (just video ID)
vidId = '4Zsaj_9Zpjc'