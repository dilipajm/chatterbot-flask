import os
import sys
print 'OS: ', os.getcwd()
import urllib
from flask import Flask, jsonify, render_template
#where chatterbot module is installed (find by running: pip instll chatterbot)
sys.path.append('/Library/Python/2.7/site-packages/')
reload(sys)
sys.setdefaultencoding('utf-8')
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import pandas as pd
import numpy as np
import datetime
import csv

app = Flask(__name__) # create a Flask app

global mybot

def print_timestamp(step='start'):
	print('-----------Step: ',datetime.datetime.now())

def get_chat_model(train=False, db='sqlite', dbname='./chatter_database.sqlite3', filename='data/studypal_faq.csv'):
	print_timestamp('get_chat_model start')

	if db == 'sqlite':
		storage_adapter = 'chatterbot.storage.SQLStorageAdapter'
	else:
		storage_adapter = "chatterbot.storage.MongoDatabaseAdapter"

	mybot = ChatBot(
	"Chat Bot",
	storage_adapter=storage_adapter,
	database=dbname,
	logic_adapters=[
		{
			"import_path": "chatterbot.logic.BestMatch",
			#"statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
			#"response_selection_method": "chatterbot.response_selection.get_first_response"
		}
	]
	)

	if (train):
		mybot = set_studypal_training(mybot, filename)
		#mybot = set_corpus_english(mybot)
		#mybot = set_corpus_movie(mybot)
	
	print_timestamp('get_chat_model end')
	return mybot

def set_corpus_english(temp_bot):
	print_timestamp('set_corpus_english start')
	temp_bot.set_trainer(ChatterBotCorpusTrainer)
	temp_bot.train(
		"chatterbot.corpus.english"
		)
	print_timestamp('set_corpus_english end')
	return temp_bot;

def set_corpus_movie(temp_bot):
	print_timestamp('set_corpus_movie start')
	filename = 'data/movie_lines.tsv'
	#filename.decode('utf-8')
	#raw_df = pd.read_csv(filename)
	#raw_df.to_csv('data/movie_lines_utf.csv',encoding='utf-8')

	#lines_df = pd.read_csv('data/movie_lines_utf.csv',sep='\t',error_bad_lines=False,warn_bad_lines =False,header=None)
	lines_df = pd.read_csv(filename,sep='\t',error_bad_lines=False,warn_bad_lines =False,header=None)
	lines_df.columns = ['lineId','chId','mId','chName','dialogue']
	print(lines_df.head())
	arr = lines_df.iloc[0:2000,4:5].values
	#print(arr)
	arr2 = []#np.digitize(lines_df.iloc[:, 4:5], bins)
	
	for index, str2 in enumerate(arr):
		str2 = str(str2[0])
		#str2 = u' '.join((str2, ' ')).encode('utf-8').strip()
		#str2 = str2.encode('utf-8').strip()
		#str2 = str2.decode('utf-8')
		print 'line ',index,' : ', str2
		arr2.append(str2)

	#print(arr2)
	print('training start')
	temp_bot.set_trainer(ListTrainer)
	temp_bot.train(arr2)
	print('training finish')
	print_timestamp('set_corpus_movie end')
	return temp_bot;

def set_studypal_training(temp_bot, csvfile):
	print_timestamp('set_studypal_training start')
	#filename = 'data/studypal_messages_text.csv'
	filename = csvfile

	rows = []
	frame_header = ['message']

	with open(filename, 'rb') as f_input:
		for row in f_input:
			rows.append(row)
			print 'line: '+row

	frame = pd.DataFrame(rows, columns=frame_header)
	print(frame.head())
	print('---------------------------------------')
	
	arr = frame.iloc[:,:].values
	arr2 = []
	
	for index, str2 in enumerate(arr):
		str2 = str(str2[0])
		print 'Index line ',index,' : ', str2
		arr2.append(str2)

	print('training start')
	#print(arr2)
	temp_bot.set_trainer(ListTrainer)
	temp_bot.train(arr2)
	print('training finish')
	print_timestamp('set_studypal_training end')
	return temp_bot;

@app.after_request
def add_header(r):
	"""
	Add headers to both force latest IE rendering engine or Chrome Frame,
	and also to cache the rendered page for 10 minutes.
	"""
	r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	r.headers["Pragma"] = "no-cache"
	r.headers["Expires"] = "0"
	r.headers['Cache-Control'] = 'public, max-age=0'
	return r

@app.route('/get_response/<path:chat>', methods=['POST'])
def get_response(chat):
	print_timestamp('get_response start')
	print chat
	chat = urllib.quote_plus(chat)
	# print chat
	# curl -X POST http://localhost:<port>/get_response/<image url>
	# http://www.isle.illinois.edu/sst/data/vgg_flickr8k.html
	# https://www.cs.toronto.edu/~frossard/vgg16/imagenet_classes.py
	print 'get_response start...'
	response = mybot.get_response(chat.lower())
	#return jsonify({'response':response.text})
	print_timestamp('get_response end')
	return response.text

@app.route('/index')
def index():
	print_timestamp('index start')
	print_timestamp('index end')
	return render_template('index.html')


if __name__ == '__main__':
  print 'initialize chat model...'

  mybot = get_chat_model(train=True) #Sqlite
  # mybot = get_chat_model(train=True, db='mongodb', dbname='studypal_faq', filename='data/studypal_faq.csv')

  #mybot.trainer.export_for_training('data/movie_dialog_export.json')
  print 'Chat model loaded...'
  app.run(debug=False, host='0.0.0.0',port=8000) # this will start a local server




