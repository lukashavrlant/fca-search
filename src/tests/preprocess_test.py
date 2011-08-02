import unittest
from preprocess.words import towords, remstopwords
from common.io import readfiles, readfile
from common.funcfun import lmap
from preprocess.index_builder import toIndex
from other.constants import TEST_FOLDER
from other.data import getStopWords

class TestWords(unittest.TestCase):
	def test_towords(self):
		self.assertEquals(['Každému', 'svítání', 'předchází', 'hluboká', 'tma...'], towords('Každému svítání předchází hluboká tma...'))
		self.assertEquals([''], towords(''))
		
	def test_remstopwords(self):
		words = 'Van Rossum was born and grew up in the Netherlands, where he received a masters degree in mathematics and computer science'.split()
		self.assertEquals(['Rossum', 'born', 'grew', 'the', 'Netherlands,', 'where', 'received', 'masters', 'degree', 'mathematics', 'computer', 'science'], list(remstopwords(words, ['Van', 'was', 'up', 'in', 'and', 'he', 'a'])))
		self.assertEquals(['Van', 'Rossum', 'was', 'born', 'and', 'grew', 'up', 'in', 'the', 'Netherlands,', 'where', 'he', 'received', 'a', 'masters', 'degree', 'in', 'mathematics', 'and', 'computer', 'science'], list(remstopwords(words, [])))
		self.assertEquals(['a', 'b'], list(remstopwords(['a', 'b'], ['c'])))
		
	def test_toIndex(self):
		urls = ['binomicka-veta.html', 'prirozena-cisla.html', 'pythagorova-veta.html', 'rovnice.html', 'zaklady-statistiky.html']
		sites = readfiles(lmap(lambda x: TEST_FOLDER + 'sites/' + x, urls))
		result = toIndex(sites, urls, [], 1)
		desired = readfile(TEST_FOLDER + 'results/index1.txt')
		self.assertEquals(repr(result), desired)
		
		result = toIndex(sites, urls, getStopWords(), 1)
		desired = readfile(TEST_FOLDER + 'results/index2.txt')
		self.assertEquals(repr(result), desired)
		
		result = toIndex(sites, urls, getStopWords(), 2)
		desired = readfile(TEST_FOLDER + 'results/index3.txt')
		self.assertEquals(repr(result), desired)
		
		#savefile(repr(toIndex(sites, urltoIndextopWords(), 2)), TEST_FOLDER + 'results/index3.txt')
		
if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()