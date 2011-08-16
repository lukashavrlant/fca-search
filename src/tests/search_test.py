import unittest
from retrieval.search_engine import SearchEngine
from other.constants import TEST_FOLDER
from other.data import getStopWords
from common.io import readfile
from retrieval.index import Index


class SearchTest(unittest.TestCase):

	def test_SearchEngine(self):
		temp = SearchEngine(Index(TEST_FOLDER + 'database/'), getStopWords()).search
		fun = lambda query: repr(temp(query)['documents'])
		ass = self.assertEquals
		read = lambda name: readfile(TEST_FOLDER + 'results/' + name + '.txt')
		
		ass(fun('nesmysl'), read('search1'))
		ass(fun('derivace'), read('search2'))
		ass(fun('rovnice'), read('search3'))
		ass(fun('nonsense'), read('search4'))
		ass(fun('derivace+mnoziny'), read('search5'))
		ass(fun('byvaji'), read('search6'))
		
		


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()