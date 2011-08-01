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
		desired_derivak = "{'count': 187, 'documents': {1: 2, 14: 2, 116: 1, 117: 3, 86: 12, 87: 4, 88: 4, 89: 5, 90: 5, 91: 45, 92: 35, 93: 18, 94: 9, 95: 42}, 'docids': dict_keys([1, 14, 116, 117, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95]), 'stem': 'derivak'}"
		desired_nonsense = "{'count': 0, 'documents': {}, 'docids': [], 'stem': ''}"
		
		self.assertEqual(repr(self.index.get_stem_info('nonsense')), desired_nonsense)
		self.assertEqual(repr(self.index.get_stem_info('derivak')), desired_derivak)
		
	def test_term_frequency(self):
		fun = self.index.term_frequency 
		self.assertEqual(fun('derivak', 117), 3)
		self.assertEqual(fun('nachazim', 76), 1)
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
		
		desired_nesmysl = "[{'url': 'http://localhost/matweb/dukaz-sporem', 'wordscount': 1231, 'id': 105}, {'url': 'http://localhost/matweb/relace', 'wordscount': 1624, 'id': 98}, {'url': 'http://localhost/matweb/co-je-to-funkce', 'wordscount': 2597, 'id': 13}, {'url': 'http://localhost/matweb/goniometricke-rovnice', 'wordscount': 775, 'id': 46}]"
		self.assertEqual(repr(fun('nesmysl')), desired_nesmysl)
		self.assertEqual(lfun('rovnice průměr'), 6)
		self.assertEqual(lfun('průměr NOT úhlopříčky'), 5)
		self.assertEqual(lfun('rovnice'), 118)
		self.assertEqual(lfun('nonsense'), 0)
		self.assertEqual(lfun('(průměry OR nesmysly) NOT derivace'), 8)
		
if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
	
	