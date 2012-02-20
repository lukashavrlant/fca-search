import unittest
from other.constants import PYTHON3, ROOT_FOLDER
from retrieval.search_engine import SearchEngine
from other.constants import TEST_FOLDER
from other.data import getStopWords
from common.io import readfile, savefile
from retrieval.index import Index
from subprocess import Popen, PIPE
from json import loads


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

		queries = {
			'poslounposti' : 'posloupnosti',
			'derivcae' : 'derivace',
			'nemsysl' : 'nesmysl',
			'hroamdny' : 'hromadny'
		}

		for k, v in queries.items():
			result = loads(self.execute('matweb', k))
			ass(result['spellcheck'][k], v)

	def execute(self, dtb, q):
		return self.runShell(dtb, q).decode("utf-8")

	def runShell(self, dtb, q):
		cmd = PYTHON3 + ROOT_FOLDER + 'src/search '
		with Popen(cmd + '-d ' + dtb + ' -q "' + q + '" -f json -t', stdout=PIPE, shell=True) as sh:
			return sh.stdout.read()
		
		


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()