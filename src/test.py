from common.io import download, savefile, readfile
import xml.etree.ElementTree as etree
from urllib.parse import quote
from other.stopwatch import Stopwatch
import pickle

def googleSearch(query, start, end):
	url = 'http://query.yahooapis.com/v1/public/yql?q='
	url += quote('select * from google.search({0},{1}) where q="{2}"'.format(start, end, query))
	url += '&format=xml&env=http%3A%2F%2Fdatatables.org%2Falltables.env'
	return download(url)

def getLinks(result):
	tree = etree.fromstring(result)
	temp = tree.findall('results/results/url')
	temp = {str(x.text) for x in temp}
	return temp

#import pickle
#
#zoit = { "Crud": "No", "Fsck": "Blox"}
#file = open("pickle.pck", "w") # write mode
#pickle.dump(zoit, file)
#
#print "Written to disk. Deleting 'zoit' now."
#del zoit
#file.close()
#del file
#print "Zoit is now deleted. Reading back from file now:"
#
#file = open("pickle.pck", "r") # read mode
#narf = pickle.load(file)
#print narf

import random
import string
import shelve

def randomText(size):
	return ''.join(random.choice(string.ascii_lowercase) for x in range(size))

def randomList(listSize, itemSize):
	return [randomText(itemSize) for x in range(listSize)]

def randomDict(dictSize):
	return {randomText(random.randint(5, 15)):randomList(random.randint(5, 15), random.randint(5, 15)) for k,v in zip(range(dictSize), range(dictSize))}

print('Done.')