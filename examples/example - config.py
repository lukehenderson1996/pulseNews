'''config.py: config constants for pulseNews'''

# Author: Luke Henderson
__version__ = '0.4'

#run/debug mode settings
jobs = ['ytTranscribe'] #list of jobs to run. Options are: ['ytTranscribe', 'pullRss', 'tweetAnalysis', 'testLogger']
logEn = False
#data sim (quickly runs without paying for API calls by using previously generated openai completions)
simulateCompletions = False

#youtube video to transcribe (just video ID)
vidId = '4Zsaj_9Zpjc'
bulletPointNum = 8 #must be int
tokensPerbp = 87 #350 tokens for four bullet points
