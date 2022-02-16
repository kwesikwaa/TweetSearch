from itertools import count
import tweepy
from decouple import config
from typing import Optional, List


apikey = config("APIKEY")
apisecret = config("APIKEY_SECRET")
access_token = config("ACCESS_TOKEN")
access_token_secret = config("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(apikey, apisecret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

def getweetkeywords(keyword: str, user: str):
    # KEYWORD WAS HAVE A MIN OF THREE CHARACTERS
    basket = []
    try:
        if(api.get_user(screen_name = user)):
            x = api.user_timeline(screen_name=user, include_rts = False, exclude_replies = True, count = 200)
            if(x is not None):
                print(f'{len(x)} tweets dey')
                print('started scanning...')
                for y in x:
                    if(y.text.lower().find(keyword.lower()) != -1):
                        basket.append(y)
                        print(y.text)
                        print(f'retweets: {y.retweet_count}')
                        print('---------------------')
                # return basket   
            else: 
                print('the person never tweet before')
            
            print(f'---{len(basket)} tweets matched the <<{keyword}>> keyword--- for user --> {user}') 
            print('---OPERATION COMPLETE---') 
    except:
        print("User like that no dey")

word = input("Enter keyword you want to ig")
getweetkeywords(keyword=word, user="NAkufoAddo")