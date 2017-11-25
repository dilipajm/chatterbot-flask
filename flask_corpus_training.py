
# coding: utf-8

# In[5]:

import os
import sys
print 'OS: ', os.getcwd()
#where chatterbot module is installed (find by running: pip instll chatterbot)
sys.path.append('/Library/Python/2.7/site-packages/') 


# In[6]:

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatterbot = ChatBot(
    "Training Example",
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": "chatterbot.response_selection.get_first_response"
        }
    ])
chatterbot.set_trainer(ChatterBotCorpusTrainer)

chatterbot.train(
    "chatterbot.corpus.english"
)


# In[ ]:

print('Discussion:')
while True:
    try:
        x = raw_input("User:");
        response = chatterbot.get_response(x.lower())
        print('Bot: ', response)
    except(KeyboardInterrupt, EOFError, SystemExit):
        break


# In[ ]:



