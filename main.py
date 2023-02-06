import tweepy
import os
from textblob import TextBlob
from dotenv import load_dotenv

# load sensitive information as enviroment variables
apiKey = os.getenv("apiKey")
apiSecret = os.getenv("apiSecret")
accessToken = os.getenv("accessToken")
accessTokenSecret = os.getenv("accessTokenSecret")
load_dotenv()

# authenticate with twitter 
auth = tweepy.OAuthHandler(apiKey, apiSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

# prompt for two team names 
firstTeamName = input("First team: ")
secondTeamName = input("Second team: ")

# search tweets for team names
firstTeamTweets = tweepy.Cursor(api.search_tweets, q=firstTeamName).items(100)
secondTeamTweets = tweepy.Cursor(api.search_tweets, q=secondTeamName).items(100)

# initialize sentiment counters
firstTeamPositiveTweets = 0
firstTeamNegativeTweets = 0
firstTeamNeutralTweets = 0
secondTeamPositiveTweets = 0
secondTeamNegativeTweets = 0
secondTeamNeutralTweets = 0

# sentiment analysis
for firstTeamTweet in firstTeamTweets:
    analysis = TextBlob(firstTeamTweet.text)
    if analysis.sentiment.polarity > 0:
        firstTeamPositiveTweets += 1
    elif analysis.sentiment.polarity < 0:
        firstTeamNegativeTweets += 1
    else:
        firstTeamNeutralTweets += 1
        
for secondTeamTweet in secondTeamTweets:
    analysis = TextBlob(secondTeamTweet.text)
    if analysis.sentiment.polarity > 0:
        secondTeamPositiveTweets += 1
    elif analysis.sentiment.polarity < 0:
        secondTeamNegativeTweets += 1
    else:
        secondTeamNeutralTweets += 1

#calculate overall sentiment
firstTeamOverall = firstTeamPositiveTweets - firstTeamNegativeTweets - (firstTeamNeutralTweets/2)
secondTeamOverall = secondTeamPositiveTweets - secondTeamNegativeTweets - (secondTeamNeutralTweets/2)

if firstTeamOverall > secondTeamOverall:
    teamDifference = firstTeamOverall - secondTeamOverall
    print (firstTeamName + " has a better overall sentiment on Twitter with a difference of " + str(teamDifference))
elif secondTeamOverall > firstTeamOverall:
    teamDifference = secondTeamOverall - firstTeamOverall
    print (secondTeamName + " has a better overall sentiment on Twitter with a difference of " + str(teamDifference))
elif firstTeamPositiveTweets > secondTeamPositiveTweets:
    teamDifference = firstTeamPositiveTweets - secondTeamPositiveTweets
    print (firstTeamName + " has more positive tweets with a difference of " + str(teamDifference))
elif secondTeamPositiveTweets > firstTeamPositiveTweets:
    teamDifference = secondTeamPositiveTweets - firstTeamPositiveTweets
    print (secondTeamName + " has more positive tweets with a difference of " + str(teamDifference))
elif secondTeamNegativeTweets > firstTeamNegativeTweets:
    teamDifference = secondTeamNegativeTweets - firstTeamNegativeTweets
    print (secondTeamName + " has more negative tweets with a difference of " + str(teamDifference))
elif firstTeamNegativeTweets > secondTeamNegativeTweets:
    teamDifference = firstTeamNegativeTweets - secondTeamNegativeTweets
    print (firstTeamName + " has more negative tweets with a difference of " + str(teamDifference))
else:
    print ("Both teams have approximately the same sentiment")
#can be optimized with functions so less crowded code
