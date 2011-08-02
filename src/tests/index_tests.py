import unittest
from retrieval.index import Index
from retrieval.boolean_parser import BooleanParser
from other.constants import TEST_FOLDER

class TestIndex(unittest.TestCase):
	databaseFolder = TEST_FOLDER + 'database/'
	index = None
	
	def setUp(self):
		self.index = Index(self.databaseFolder)
	
	def test_get_stem_info(self):
		fun = lambda stem: repr(self.index.get_stem_info(stem))
		desired_derivak = "{'count': 187, 'documents': {65: 45, 67: 9, 38: 4, 103: 12, 105: 5, 10: 35, 43: 2, 109: 2, 110: 5, 81: 4, 20: 1, 86: 3, 55: 42, 42: 18}, 'docids': dict_keys([65, 67, 38, 103, 105, 10, 43, 109, 110, 81, 20, 86, 55, 42]), 'stem': 'derivak'}"
		desired_nonsense = "{'count': 0, 'documents': {}, 'docids': [], 'stem': ''}"
		
		self.assertEqual(fun('nonsense'), desired_nonsense)
		self.assertEqual(fun('derivak'), desired_derivak)
		
	def test_term_frequency(self):
		fun = self.index.term_frequency 
		
		self.assertEqual(fun('derivak', 81), 4)
		self.assertEqual(fun('nachazim', 73), 1)
		self.assertEqual(fun('nonsense', 1), 0)
		self.assertEqual(fun('nonsense', 100000), 0)
		
	def test_document_frequency(self):
		fun = self.index.document_frequency
		self.assertEqual(fun('nachazim'), 2)
		self.assertEqual(fun('derivak'), 14)
		self.assertEqual(fun('nonsense'), 0)
		
	def test_get_documents(self):
		parse = BooleanParser().parse
		fun = lambda x: self.index.get_documents(parse(x))
		lfun = lambda x: len(fun(x))
		
		desired_nesmysl = "[{'url': 'http://localhost/matweb/dukaz-sporem', 'keywords': ['prvocisl', 'tvrzen', 'prvocisel', 'spor', 'nezajimav', 'prvociseln', 'rozklad', 'posloupnost', 'zajimav', 'nejmens'], 'wordscount': 909, 'id': 64}, {'url': 'http://localhost/matweb/goniometricke-rovnice', 'keywords': ['sin', 'substituk', 'cos', 'kosin', 'goniometrick', 'spoctet', 'rovnic', 'jiz', 'graf', 'resil'], 'wordscount': 568, 'id': 80}, {'url': 'http://localhost/matweb/co-je-to-funkce', 'keywords': ['vstup', 'vystup', 'parametr', 'vrat', 'argument', 'autom', 'tabulk', 'hodnot', 'funkcn', 'sloupeck'], 'wordscount': 1788, 'id': 34}, {'url': 'http://localhost/matweb/relace', 'keywords': ['relak', 'honzik', 'sandr', 'josef', 'usporadan', 'reflexivn', 'dvojik', 'transitivn', 'symetrick', 'binarn'], 'wordscount': 1127, 'id': 93}]"
		self.assertEqual(repr(fun('nesmysl')), desired_nesmysl)
		self.assertEqual(lfun('rovnice průměr'), 6)
		self.assertEqual(lfun('průměr NOT úhlopříčky'), 5)
		self.assertEqual(lfun('rovnice'), 114)
		self.assertEqual(lfun('nonsense'), 0)
		self.assertEqual(lfun('(průměry OR nesmysly) NOT derivace'), 8)
		
if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
	
	