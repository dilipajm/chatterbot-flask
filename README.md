
# install chatterbot
pip install chatterbot

# In init method, api_chatbot
For sqlite db,
mybot = get_chat_model(train=True) #Sqlite

For mongodb,
mybot = get_chat_model(train=True, db='mongodb', dbname='studypal_faq', filename='data/studypal_faq.csv')

# install mongodb
brew update
brew install mongodb

# run server
python api_chatbot.py

==========================

# Errors

1. pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [Errno 61] Connection refused
Start mongodb - brew services start mongodb
or Install mongodb
