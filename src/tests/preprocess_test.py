import unittest
from preprocess.words import towords, remstopwords
from common.io import readfiles, readfile, savefile
from common.funcfun import lmap
from preprocess.index_builder import toIndex
from other.constants import TEST_FOLDER, DATA_FOLDER
from other.data import getStopWords
from common.io import downloads

class TestWords(unittest.TestCase):
	def test_towords(self):
		self.assertEqual(['Každému', 'svítání', 'předchází', 'hluboká', 'tma...'], towords('Každému svítání předchází hluboká tma...'))
		self.assertEqual([''], towords(''))
		
	def test_remstopwords(self):
		words = 'Van Rossum was born and grew up in the Netherlands, where he received a masters degree in mathematics and computer science'.split()
		self.assertEqual(['Rossum', 'born', 'grew', 'the', 'Netherlands,', 'where', 'received', 'masters', 'degree', 'mathematics', 'computer', 'science'], list(remstopwords(words, ['Van', 'was', 'up', 'in', 'and', 'he', 'a'])))
		self.assertEqual(['Van', 'Rossum', 'was', 'born', 'and', 'grew', 'up', 'in', 'the', 'Netherlands,', 'where', 'he', 'received', 'a', 'masters', 'degree', 'in', 'mathematics', 'and', 'computer', 'science'], list(remstopwords(words, [])))
		self.assertEqual(['a', 'b'], list(remstopwords(['a', 'b'], ['c'])))
		
	def test_toIndex(self):
		urls = self.getURLs()
		sites = downloads(urls)
		sites = [{'type':'html', 'content':x, 'url':'url'} for x in sites]
		
		# savefile(repr(toIndex(sites, [], 1)), TEST_FOLDER + 'index1.txt')
		# savefile(repr(toIndex(sites, getStopWords(), 1)), TEST_FOLDER + 'index2.txt')
		# savefile(repr(toIndex(sites, getStopWords(), 2)), TEST_FOLDER + 'index3.txt')
		
		result = toIndex(sites, [], 1)
		desired = readfile(TEST_FOLDER + 'index1.txt')
		self.assertEqual(repr(result), desired)
		
		result = toIndex(sites, getStopWords(), 1)
		desired = readfile(TEST_FOLDER + 'index2.txt')
		self.assertEqual(repr(result), desired)
		
		result = toIndex(sites, getStopWords(), 2)
		desired = readfile(TEST_FOLDER + 'index3.txt')
		self.assertEqual(repr(result), desired)

	def getURLs(cls):
		path = DATA_FOLDER + 'test.txt'
		content = readfile(path).splitlines()
		return content	
		
if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()