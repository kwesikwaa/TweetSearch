#RECEIPT CENTRAL
enter a twitter user name and keyword search through their tweets.

demo on: https://receiptcentral.pages.dev

The frontend is vanilla html/css and alpine js.

The Python backend uses the tweepy api
The backend is hosted on AWS Lambda. 

FastAPI restapi was for development only.

The way to get the code onto Lambda is to zip the py file together with installed dependencies and imported into Lambda.

to install dependencies into the folder
cd into the parent folder and pip install --target=name_of_dependency_folder tweepy
add the py file to that content and then zip it

DONE !!!