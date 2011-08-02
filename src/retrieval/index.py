from common.io import readfile
from retrieval.record import Record
from functools import reduce
from operator import and_, or_
from common.funcfun import lmap
from retrieval.boolean_parser import Node
from other.constants import INDEX_FOLDER_NAME, DOCUMENT_INFO_NAME, INFO_FOLDER_NAME
from preprocess.words import getstem

class Index:
	
	def __init__(self, directory, documentsInfo = None):
		self.dtb = {}
		self.keylen = 1
		self.total_records = 0
		self.directory = directory
		self.documents_info = documentsInfo if documentsInfo else self._get_translation()
		self.total_records = len(self.documents_info)
		
	def get_documents(self, parsedQuery):
		documents = self._by_node(parsedQuery)
		return lmap(self._translate, documents)
	
	def get_stem_info(self, stem):
		return self._get_record(stem[:self.keylen]).stem(stem)
	
	def term_frequency(self, term, documentID):
		return self.get_stem_info(term).documents.get(documentID, 0)
	
	def document_frequency(self, term):
		return len(self.get_stem_info(term).documents)
	
	def getKeywords(self, docID):
		return self.documents_info[docID]['keywords']
		
	def _by_node(self, node):
		if isinstance(node, Node):
			if node.type == 'AND':
				return self._by_and_node(node.children)
			if node.type == 'OR':
				return self._by_or_node(node.children)
			if node.type == 'NOT':
				return self._by_not_node(node.children[0])
		else:
			return self._by_word(node)
		
	def _by_and_node(self, children):
		return reduce(and_, map(self._by_node, children))
	
	def _by_or_node(self, children):
		return reduce(or_, map(self._by_node, children))
	
	def _by_not_node(self, argument):
		allDocuments = set(range(len(self.documents_info)))
		matchedDoc = self._by_node(argument)
		return allDocuments - matchedDoc 
	
	def _by_words(self, words):
		return lmap(self._translate, reduce(and_, map(self._by_word, words)))
	
	def _by_word(self, word):
		stem = getstem(word) 
		record = self._get_record(stem[:self.keylen])
		
		if record:
			documents = record.stem(stem)
			if documents:
				return set(documents.docids)

		return set()
		
		
	def _get_record(self, prefix):
		return self.dtb.get(prefix) or self._load_record(prefix)
		
	def _load_record(self, prefix):
		try:
			record = Record(readfile(self.directory + INDEX_FOLDER_NAME + prefix + '.txt'))
		except:
			record = Record('')
		
		self.dtb[prefix] = record
		return record
	
	def _get_translation(self):
		return eval(readfile(self.directory + INFO_FOLDER_NAME + DOCUMENT_INFO_NAME))
	
	def _translate(self, docid):
		return self.documents_info[docid]