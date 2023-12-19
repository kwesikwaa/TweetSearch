import tweepy
from decouple import config
from typing import Optional
from pydantic import BaseModel
from typing import List

from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

apikey = config("APIKEY")
apisecret = config("APIKEY_SECRET")
access_token = config("ACCESS_TOKEN")
access_token_secret = config("ACCESS_TOKEN_SECRET")
bearer = config('bear')

# client = tweepy.Client(bearer_token=bearer,consumer_key=apikey,consumer_secret=apisecret,access_token=access_token, access_token_secret=access_token_secret)
# client = tweepy.Client(bearer_token=bearer)

# auth = tweepy.OAuth2BearerHandler(bearer)

# auth = tweepy.OAuth1UserHandler(apikey,apisecret,access_token,access_token_secret)
# auth = tweepy.OAuthHandler(apikey, apisecret)  old 
auth = tweepy.OAuth2AppHandler(apikey, apisecret)
# auth.set_access_token(access_token,access_token_secret)


api = tweepy.API(auth)

class Tweetdantic(BaseModel):
    dp: str
    at: str
    name: str
    likes: int
    retweets: int
    tweet: str
    url: str
    date: str

class Tweetrequest(BaseModel):
    at: str
    keyword: str
    addrts: Optional[bool]=True



t = ('%a %d %b,%Y %I:%M %p')
# m = api.mentions_timeline()
#
# probably serve the html with jinja 

# API 

@app.post('/api/v1/search', response_model=List[Tweetdantic])
async def getresults(inputs: Tweetrequest):
    basket = []

    print(api.get_user(username=inputs.at))
    print(inputs)
    # user = await api.get_user(screen_name=inputs.at)
    # if user:
    # await diggint(inputs,basket)
    
    
    

async def diggint(inputs,basket):
    print('in diggi')
    x = await api.user_timeline(screen_name=inputs.at, include_rts = inputs.addrts,count = 20)
    print(len(x))
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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Sorry, there is no such tweet")                                     
        return basket  
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Sorry there are zero tweets from this handle")            

