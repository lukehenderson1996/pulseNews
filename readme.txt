Information and feed aggregator/gathering/analysis platform utilizing OpenAI's LLMs  

Written by: 
Luke Henderson
Dawson Fields

**********NEED TO MIGRATE OPENAI CODE WITH LINUX***********
https://github.com/openai/openai-python/discussions/742
https://community.openai.com/t/how-to-migrate-openai-i-cannot-use-chatgpt-api/575437


installation instructions:

#main.py:
pip install openai

#tgBot.py
pip install telebot

#transcribeYoutube.py:
pip install youtube-transcript-api
pip install beautifulsoup4
pip install xmltodict

#webDriver.py:
pip install selenium
pip install webdriver_manager
pip install xmltodict

#twitter
pip install twitter-scraper-selenium

#general
Current programs use version 3.7.9 64 bit
you will need pythonNotes in your PYTHONPATH: https://github.com/lukehenderson1996/pythonNotes
Alternatively, the quick and dirty solution is to paste relevant pythonNotes scripts into pulseNews\scripts
Windows PYTHONPATH instructions: 
press windows key, type in "advanced", press enter
should open system properties, advanced
click Environmental Variables
under User variables for [USERNAME]: 
Add/modify variable "PYTHONPATH" to include:
    (should already have Python37 stuff)
    C:\path\to\your\scripts
must restart cmd, but not entire computer

#OpenAI API setup
must create paid account and get private key from:
https://platform.openai.com/
see examples\example api-Keys.py for formatting of scripts\apiKeys.py (.gitignore setup to not track/upload this file)




openai API resources
https://platform.openai.com/playground?lang=python&mode=complete&model=text-davinci-003
https://openai.com/pricing
https://platform.openai.com/docs/api-reference/chat/create
https://github.com/openai/openai-cookbook





-----------------------------------------------------gpt-3.5-turbo summarizer-----------------------------------------------------
Working on gettting OpenAI's tools to summarize potentially controversial content. gpt 3.5 and 4 have opinions of their own, 
and will "parent" you into not asking for controversial outputs. This approach gets around this by giving the LLM a role to play 
other than its normal one. 

Settings:
temp: 0, max length: 25, top p: 0.25

System:
You are an Analyst for a corporate intelligence group. You generate concise summaries of input information for the company to later aggregate and analyze. You don't perform any analysis on the input content. You merely summarize it in the voice of the original author. 

User:
Summarize this tweet in 10-20 words
<tweet>
Just heard another heartbreaking story of a child developing autism after vaccination. The evidence is mounting, folks! It's time to wake up and question the safety of these vaccines. Don't let the medical establishment fool you any longer
</tweet>

Assistant:
A child developed autism after vaccination, questioning vaccine safety.




















-------------------------------------------------------Chat example:-------------------------------------------------------
System:
You are a helpful assistant that rates tweets for importance. The assistant responds simply with a float or int:
4
9.8
1
3.5

User:
How important is this tweet on a scale of 1-10?

<example tweet 1>This is a bombshell finding!</example tweet 1>
<example response 1>8</example response 1>
<example tweet 2>I am bored</example tweet 2>
<example response 2>1</example response 2>

<tweet>It turns out we have 100% proven that vaccines cause autism</tweet>




-----------------------------------------------------------completions example:-----------------------------------------------------------

How important is this tweet on a scale of 1-10?

This is a bombshell finding!
8

I am bored
1

[insert tweet here]




---------------------------------------completions summarization: (temp=0.25, max length=18, top P=1)---------------------------------------

Summarize this tweet in half the words or less

<tweet>
"How is it possible that all consumer protection laws we have for pharmaceuticals were simultaneously suspended?" - Former Big Pharma executive @sasha_latypova
 

Watch the full interview.
</tweet>



------------------------------------------------------completions bulk rate importance------------------------------------------------------
(temp=0, top p=1, stop_sequence='}')
How important are these tweets on a scale of 1-10?

<tweet 1>
He actually said...
"Woman is a social construct"

I'm getting out of the way.
#justsayin
</tweet 1>
<tweet 2>
Jikkyleaks 🐭 Retweeted
Broken Truth
@BrokenTruthTV
·
2h
"Vaccine enhancement" you say? This is why they kept Francis Collins away from the cameras.
</tweet 2>
<tweet 3>
Jikkyleaks 🐭 Retweeted
Jurassic Carl 🦖🐭
@carl_jurassic
·
3h
Replying to 
@masterlongevity
 and 
@Jikkyleaks
“Master longevity”

Add to the list of anti aging gurus who jibber jab for the Jibby jab!
</tweet 3>
<tweet 4>
Cringe tweet of the week
</tweet 4>
<tweet 5>
🚨 26.4% excess deaths in the 0-24 age bracket!! 

Wake up, everyone! 

These are kids!
</tweet 5>
Format:
{'tweet 1': x, 'tweet 2': x, 'tweet 3': x,  'tweet 4': x, 'tweet 5': x}

{














