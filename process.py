import json
import csv
from pprint import pprint
from pymongo import MongoClient


client = MongoClient("mongodb://xiang:1@ds149437.mlab.com:49437/twitter_db")
db = client.twitter_db
collection = db.twitter_collection

def wordscount():
	textdata = []
	rownum = 1
	with open('./MiningTwitterData/pokemon.json') as data_file:
		for line in data_file: 
			if((rownum % 2) == 1):
		    		data = json.loads(line)
				textdata.append(data['text'])
			rownum += 1

	from nltk.tokenize import RegexpTokenizer
	from stop_words import get_stop_words
	from nltk.stem.porter import PorterStemmer

	allwords=[]
	tokenizer = RegexpTokenizer(r'\w+')
	for num in range(len(textdata)):
		raw = textdata[num].lower()
		tokens = tokenizer.tokenize(raw)
		en_stop = get_stop_words('en')
		stopped_tokens = [i for i in tokens if (len(i)>3 and len(i)<20 and not i in en_stop)]
		allwords.append(stopped_tokens)

	import itertools
	newAllwords = list(itertools.chain.from_iterable(allwords))

	totaldict = sorted(set(newAllwords))

	from collections import Counter
	aa = Counter(newAllwords)    #aa is a dictionary{"word": num}
	return aa

def getallpokenames():
	list = []
	with open('./data/Count.csv', 'rb') as f:
	    reader = csv.reader(f)
	    for row in reader:
		list.append(row[1])
	list = list[1:]
	return list

def countTweets(name):
    tweets_iterator = collection.find({'text': {'$regex': name}})
    count = 0
    for tweet in tweets_iterator:
        count = count + 1
    return count

def getPokeTwitter(name):
    res=[]
    tweets_iterator = collection.find({'text': {'$regex': name}}).limit(10)
    for tweet in tweets_iterator:
        res.append(tweet['text'])
    return res

print(getPokeTwitter("kakuna"))




