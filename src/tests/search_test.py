import unittest
from retrieval.search_engine import SearchEngine
from other.constants import TEST_FOLDER
from other.data import getStopWords
from common.io import readfile
from retrieval.index import Index
from subprocess import Popen, PIPE


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
		
	def testSearchCommand(self):
		path = TEST_FOLDER + 'results/'
		cmd = '/Users/lukashavrlant/Python/fca-search/src/search '
		fun = lambda dtb, q: (Popen(cmd + '-d ' + dtb + ' -q "' + q + '" nt', stdout=PIPE, shell=True).stdout.read())
		dfun = lambda dtb, q: fun(dtb, q).decode("utf-8")
		#save = lambda cont, name: savefile(cont, path + name + '.txt', False)
		read = lambda name: readfile(path + name + '.txt')
		ass = self.assertEquals
		
		ass(dfun('matweb', 'derivace'), read('derivace'))
		ass(dfun('matweb', 'nesmysl'), read('nesmysl'))
		ass(dfun('matweb', '(spocetne OR nespocetne) mnoziny'), read('spocetne'))
		ass(dfun('jpw', 'input NOT select'), read('input'))
		ass(dfun('inf', 'belohlavek'), read('belohlavek'))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()