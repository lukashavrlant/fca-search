from functools import reduce
from operator import and_, or_
from common.funcfun import lmap
from retrieval.boolean_parser import Node
import shelve
from other.constants import INDEX_FOLDER_NAME, DOCUMENT_INFO_NAME, INFO_FOLDER_NAME, STEMSDICT_NAME,\
	KEYWORDSINDOCUMENTS_NAME
from retrieval.stem import Stem

class Index:
	
	def __init__(self, directory, documentsInfo = None):
		self.info = shelve.open(directory + INFO_FOLDER_NAME + 'info')
		self.keylen = 1
		self.directory = directory
		self.documents_info = documentsInfo if documentsInfo else self._get_translation()
		self.total_records = len(self.documents_info)
		self.stemsDict = None
		self.docKeywords = None
		self.allKeywords = None
		self.searchedStem = {}
		
		
	def get_documents(self, parsedQuery):
		documents = self._by_node(parsedQuery)
		return lmap(self._translate, documents)
	
	def get_stem_info(self, stem):
		stemObject = self.searchedStem.get(stem, False)
		if stemObject:
			return stemObject
		else:
			prefix = stem[:self.keylen]
			sh = shelve.open(self.directory + INDEX_FOLDER_NAME + '/' + prefix)
			try:
				record = sh[stem]
				stemObject = Stem()
				stemObject.name = stem
				stemObject.documents = dict(record)
				stemObject.docids = stemObject.documents.keys()
				self.searchedStem[stem] = stemObject
			except KeyError:
				stemObject = Stem()
			return stemObject
	
	def term_frequency(self, term, documentID):
		stem = self.get_stem_info(term)
		documents = stem.documents
		freq = documents.get(documentID, 0)
		return freq
	
	def contains_term(self, term, documentID):
		if not self.docKeywords:
			temp = self.info[KEYWORDSINDOCUMENTS_NAME] 
			self.docKeywords = temp['inDocuments']
			self.allKeywords = temp['keywords']
		
		if term in self.allKeywords:
			return term in self.docKeywords[documentID]
		else:
			return self.term_frequency(term, documentID) > 0
	
	def document_frequency(self, term):
		return len(self.get_stem_info(term).documents)
	
	def getKeywords(self, docID):
		return self.documents_info[docID]['keywords']
	
	def stem2word(self, stem):
		if not self.stemsDict:
			self.stemsDict = self.info[STEMSDICT_NAME] 
			
		return self.stemsDict.get(stem, stem)
		
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
	
	def _by_word(self, stem):
		documents = self.get_stem_info(stem)
		return documents.docids
	
	def _get_translation(self):
		return self.info[DOCUMENT_INFO_NAME] 
	
	def _translate(self, docid):
		return self.documents_info[docid]