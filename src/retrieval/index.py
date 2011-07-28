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
		syntacticTree = self.parser.parse(query)
		documents = self._by_node(syntacticTree)
		links = lmap(self._translate, documents)
		return links
		
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
		allDocuments = set(range(len(self.translation)))
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
			record = Record(readfile(self.directory + 'index/' + prefix + '.txt'))
		except:
			record = None
		
		self.dtb[prefix] = record
		return record
	
	def _get_translation(self):
		return eval(readfile(self.directory + 'info/translation.txt'))
	
	def _translate(self, docid):
		return self.translation[docid]