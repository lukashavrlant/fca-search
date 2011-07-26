from common.io import readfile
from retrieval.record import Record
from functools import reduce
from operator import and_, or_
from common.funcfun import lmap
from retrieval.boolean_parser import Node
from preprocess.index_builder import getstem

class Index:
	dtb = {}
	
	def __init__(self, directory, parser, keylen = 1):
		self.directory = directory
		self.parser = parser
		self.keylen = keylen
		self.translation = self._get_translation()
		
	def get_documents(self, query):
		#stems = get_words(normalize_text(query))
		syntacticTree = self.parser.parse(query)
		documents = self._get_documents_for_node(syntacticTree)
		links = lmap(self._translate, documents)
		return links
		
	def _get_documents_for_node(self, node):
		if isinstance(node, Node):
			if node.type == 'AND':
				return self._get_document_for_node_and(node.children)
			if node.type == 'OR':
				return self._get_document_for_node_or(node.children)
		else:
			return self._get_documents_for_word(node)
		
	def _get_document_for_node_and(self, children):
		return reduce(and_, map(self._get_documents_for_node, children))
	
	def _get_document_for_node_or(self, children):
		return reduce(or_, map(self._get_documents_for_node, children))
	
	def _get_documents_for_words(self, words):
		return lmap(self._translate, reduce(and_, map(self._get_documents_for_word, words)))
	
	def _get_documents_for_word(self, word):
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
			record = Record(readfile(self.directory + prefix + '.txt'))
		except:
			record = None
		
		self.dtb[prefix] = record
		return record
	
	def _get_translation(self):
		return eval(readfile(self.directory + 'translation.txt'))
	
	def _translate(self, docid):
		return self.translation[docid]