import os
import sys
print 'OS: ', os.getcwd()
import urllib
from flask import Flask, jsonify, render_template
#where chatterbot module is installed (find by running: pip instll chatterbot)
sys.path.append('/Library/Python/2.7/site-packages/') 
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__) # create a Flask app

global mybot

def get_chat_model():
	mybot = ChatBot(
	"Chat Bot",
	logic_adapters=[
		{
			"import_path": "chatterbot.logic.BestMatch",
			"statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
			"response_selection_method": "chatterbot.response_selection.get_first_response"
		}
	])

	mybot.set_trainer(ChatterBotCorpusTrainer)

	mybot.train(
		"chatterbot.corpus.english"
		)
	return mybot

@app.route('/get_response/<path:chat>', methods=['POST'])
def get_response(chat):
	print chat
	chat = urllib.quote_plus(chat)
	print chat
	# curl -X POST http://localhost:<port>/get_response/<image url>
	# http://www.isle.illinois.edu/sst/data/vgg_flickr8k.html
	# https://www.cs.toronto.edu/~frossard/vgg16/imagenet_classes.py
	print 'get_response start...'
	response = mybot.get_response(chat.lower())
	return jsonify({'response':response.text})




if __name__ == '__main__':
  print 'initialize chat model...'
  mybot = get_chat_model()
  print 'Chat model loaded...'
  app.run(debug=True, host='0.0.0.0',port=7000) # this will start a local server




