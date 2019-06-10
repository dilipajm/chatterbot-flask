
# Chatbot using Flask & Chatterbot

## Install chatterbot & flask
pip install chatterbot
pip install flask

## In init method, api_chatbot
For sqlite db,
mybot = get_chat_model(train=True) #Sqlite

## For mongodb,
mybot = get_chat_model(train=True, db='mongodb', dbname='pal_faq', filename='data/pal_faq.csv')

## Install mongodb
brew update
brew install mongodb

## Run server
python api_chatbot.py

==========================

## Errors

1. pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [Errno 61] Connection refused
Start mongodb - brew services start mongodb
or Install mongodb
