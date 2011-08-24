import unittest
from retrieval.search_engine import SearchEngine
from other.constants import TEST_FOLDER
from other.data import getStopWords
from common.io import readfile, savefile
from retrieval.index import Index
from subprocess import Popen, PIPE


class SearchTest(unittest.TestCase):
		
	def testSearchCommand(self):
		path = TEST_FOLDER + 'results/'
		cmd = '/Users/lukashavrlant/Python/fca-search/src/search '
		fun = lambda dtb, q: (Popen(cmd + '-d ' + dtb + ' -q "' + q + '" -f json', stdout=PIPE, shell=True).stdout.read())
		dfun = lambda dtb, q: fun(dtb, q).decode("utf-8")
		save = lambda cont, name: savefile(cont, path + name + '.txt', False)
		read = lambda name: readfile(path + name + '.txt')
		ass = self.assertEquals
		
		
		dtbs = ['matweb', 'matweb', 'matweb', 'jpw']
		queries = ['derivace', 'nesmysl', '(spocetne OR nespocetne) mnoziny', 'input NOT select']
		filenames = ['derivace', 'nesmysl', 'spocetne', 'input']
		
		for d, q, f in zip(dtbs, queries, filenames):
			#save(fun(d, q), f)
			ass(dfun(d, q), read(f))
		
		


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()