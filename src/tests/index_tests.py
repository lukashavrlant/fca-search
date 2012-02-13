import unittest
from retrieval.index import Index
from retrieval.boolean_parser import BooleanParser
from other.constants import TEST_FOLDER, DATA_FOLDER, DATABASES_FOLDER
from other.settings import Settings
from preprocess.index_manager import IndexManager
from glob import glob
from common.io import md5

class TestIndex(unittest.TestCase):
	databaseFolder = DATABASES_FOLDER + 'test/'
	index = None
	
	@classmethod
	def setUpClass(cls):
		settings = Settings(DATA_FOLDER + 'settings.json')
		urls = cls.getURLs()
		manager = IndexManager(settings)
		manager.build(urls, cls.databaseFolder, [])
		cls.index = Index(cls.databaseFolder, settings)

	@classmethod
	def getURLs(cls):
		path = '/Users/lukashavrlant/WebSites/test-fca-search/'
		absolute = glob(path + '*')
		absolute = [x.replace(path, 'http://localhost/test-fca-search/') for x in absolute]
		return absolute

	
	def test_get_stem_info(self):
		fun = lambda stem: str(self.index.get_stem_info(stem))
		desired_derivak = "{'documents': {0: 5, 2: 45, 4: 4}, 'docids': {0, 2, 4}, 'stem': 'derivak'}"
		desired_nonsense = "{'documents': {}, 'docids': set(), 'stem': ''}"
		self.assertEqual(fun('nonsense'), desired_nonsense)
		self.assertEqual(fun('derivak'), desired_derivak)

	def test_hash_value(self):
		self.assertEqual('fc08a1834a89c01c5b09e3f010ab4094', md5(self.databaseFolder + 'info.db'))
		
	def test_term_frequency(self):
		fun = self.index.term_frequency 
		
		self.assertEqual(fun('derivak', 4), 4)
		self.assertEqual(fun('nonsense', 1), 0)
		self.assertEqual(fun('nonsense', 100000), 0)
		
	def test_document_frequency(self):
		fun = self.index.document_frequency

		self.assertEqual(fun('nachazim'), 1)
		self.assertEqual(fun('derivak'), 3)
		self.assertEqual(fun('nonsense'), 0)
		
	def test_get_documents(self):
		parse = BooleanParser().parse
		fun = lambda x: self.index.get_documents(parse(x))
		lfun = lambda x: len(fun(x))
		
		self.assertEqual(lfun('rovnice průměr'), 1)
		self.assertEqual(lfun('průměr NOT úhlopříčky'), 1)
		self.assertEqual(lfun('rovnice'), 8)
		self.assertEqual(lfun('rovnice NOT spojitost'), 5)
		self.assertEqual(lfun('(statistika OR pythagorova)'), 3)

if __name__ == '__main__':
    unittest.main()
	