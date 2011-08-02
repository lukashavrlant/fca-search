import unittest
from retrieval.search_engine import SearchEngine
from other.constants import TEST_FOLDER
from other.data import getStopWords
from common.io import readfile


class SearchTest(unittest.TestCase):

	def test_SearchEngine(self):
		temp = SearchEngine(TEST_FOLDER + 'database/', getStopWords()).search
		fun = lambda query: repr(temp(query))
		ass = self.assertEquals
		read = lambda name: readfile(TEST_FOLDER + 'results/' + name + '.txt')
		
		ass(fun('nesmysl'), read('search1'))
		ass(fun('derivace'), read('search2'))
		ass(fun('rovnice'), read('search3'))
		ass(fun('nonsense'), read('search4'))
		
		


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()