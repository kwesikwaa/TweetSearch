import tweepy
import os
import json
from pydantic import BaseModel

class Tweetdantic(BaseModel):
    dp: str
    at: str
    name: str
    likes: int
    retweets: int
    tweet: str
    url: str
    date: str


apikey = os.environ["APIKEY"]
apisecret = os.environ["APIKEY_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]
bearer = os.environ['bear']


auth = tweepy.OAuth1UserHandler(consumer_key=apikey,consumer_secret=apisecret, access_token=access_token, access_token_secret=access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)

basket = []
t = ('%a %d %b,%Y %I:%M %p')

def lambda_handler(event):
    
    actionarea(json.loads(event['body']))



def actionarea(inputs):
    x = api.user_timeline(screen_name=inputs.at, include_rts = inputs.addrts,count = 20)
    if(x is not None):
        for y in x:
            if(y.text.lower().find(inputs.keyword.lower()) != -1):
                a = Tweetdantic(
                    dp = y.user.profile_image_url,
                    at = y.user.screen_name,
                    name = y.user.name,
                    likes = y.favorite_count,
                    retweets = y.retweet_count,
                    tweet = y.text,
                    url = '',
                    date = y.created_at.strftime(t)
                )
                basket.append(a)
        if(len(basket)==0):
            return {
                'statusCode':404,
                'body':json.dumps('No tweet Found')
            }
        return {
            'statusCode':200,
            'body':json.dumps(basket)
        }
    return {
        'statusCode':404,
        'body':json.dumps("Sorry there are zero tweets from this handle")
    }
