import tweepy
from decouple import config
from typing import Optional
from pydantic import BaseModel
from typing import List

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

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

auth = tweepy.OAuthHandler(apikey, apisecret)
auth.set_access_token(access_token,access_token_secret)

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

# API 


@app.get('/')
def initt():
    return{"Asay": "Akwaaba"}


@app.post('/api/v1/search', response_model=List[Tweetdantic])
async def getresults(inputs: Tweetrequest):
    basket = []
    try:
        api.get_user(screen_name = inputs.at)   
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Sorry invalid handle")                    
    else:
        x = api.user_timeline(screen_name=inputs.at, include_rts = inputs.addrts,count = 500)
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

