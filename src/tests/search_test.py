import unittest
from other.constants import PYTHON3, ROOT_FOLDER
from retrieval.search_engine import SearchEngine
from other.constants import TEST_FOLDER
from other.data import getStopWords
from common.io import readfile, savefile
from retrieval.index import Index
from subprocess import Popen, PIPE
from json import loads
from other.interface import searchQuery

class SearchTest(unittest.TestCase):
	def testSearchCommand(self):
		path = TEST_FOLDER 
		fun = self.runShell
		dfun = lambda dtb, q: fun(dtb, q).decode("utf-8")
		save = lambda cont, name: savefile(cont, path + name + '.txt', False)
		read = lambda name: readfile(path + name + '.txt')
		ass = self.assertEqual
		
		# search matweb
		queries = ['derivace', 'nesmysl', '(spocetne OR nespocetne) mnoziny', 'rovnice', 'rovnice NOT (linearni OR pravdepodobnost)']

		ass(dfun('matweb-test', 'derivace'), read('matweb0'))
		ass(dfun('matweb-test', 'nesmysl'), read('matweb1'))
		ass(dfun('matweb-test', '(spocetne OR nespocetne) mnoziny'), read('matweb2'))
		# ass(dfun('matweb-test', 'rovnice'), read('matweb3'))
		ass(dfun('matweb-test', 'rovnice NOT (linearni OR pravdepodobnost)'), read('matweb4'))


		# for num, q in enumerate(queries):
		# 	filename = 'matweb' + str(num)
		# 	save(fun('matweb', q), filename)

	def test_spellcheck(self):
		ass = self.assertEqual
		fun = lambda q: searchQuery('matweb-test', q)['suggestions'][q]

		ass(fun('poslounposti'), 'posloupnosti')
		ass(fun('derivcae'), 'derivace')
		ass(fun('nemsysl'), 'nesmysl')
		ass(fun('hroamdny'), 'hromadny')


	def test_Generalization(self):
		ass = self.assertEqual
		fun = lambda q: searchQuery('matweb-test', q)['generalization']

		ass(fun('inverzni mnoziny prvky'), [{'words': ['inverzni'], 'rank': 24}, {'words': ['prvky'], 'rank': 20}, {'words': ['mnoziny'], 'rank': 19}])
		ass(fun('derivace'), [])
		ass(fun('bod hokus'), [{'words': ['hokus'], 'rank': 1}])

	def test_Specialization(self):
		ass = self.assertEqual
		fun = lambda q: searchQuery('matweb-test', q)['specialization']

		ass(fun('derivace'), [{'rank': 13, 'words': ['limita']}, {'rank': 12, 'words': ['posloupnosti']}, {'rank': 10, 'words': ['bodě']}, {'rank': 3, 'words': ['symboly']}])
		ass(fun('Pravděpodobnost OR množiny'), [{'rank': 6, 'words': ['hesla']}, {'rank': 5, 'words': ['lidí']}, {'rank': 4, 'words': ['kostce']}])
		ass(fun('kravina'), [])


	def execute(self, dtb, q):
		return self.runShell(dtb, q).decode("utf-8")

	def runShell(self, dtb, q):
		cmd = PYTHON3 + ROOT_FOLDER + 'src/search '
		with Popen(cmd + '-d ' + dtb + ' -q "' + q + '" -f json -t', stdout=PIPE, shell=True) as sh:
			return sh.stdout.read()
		
		


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()