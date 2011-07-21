from common.io import readfile
from retrieval.record import Record
from functools import reduce
from operator import and_
from common.funcfun import lmap
from common.string import normalize_text
from preprocess.words import get_words

class Index:
	dtb = {}
	
	def __init__(self, directory, keylen = 1):
		self.directory = directory
		self.keylen = keylen
		self.translation = self._get_translation()
		
	def get_documents(self, query):
		stems = get_words(normalize_text(query))
		return lmap(self._translate, reduce(and_, map(self._get_documents, stems)))
	
	def _get_documents(self, stem):
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