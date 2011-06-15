from common.io import readfile
from retrieval.record import Record
from functools import reduce
from operator import and_

class Index:
	def __init__(self, directory, keylen = 1):
		self.dtb = {}
		self.directory = directory
		self.keylen = keylen
		
	def get_documents(self, stems):
		return reduce(and_, map(self._get_documents, stems))
	
	def _get_documents(self, stem):
		record = self._get_record(stem[:self.keylen])
		return set(record.stem(stem).docids)
		
	def _get_record(self, prefix):
		return self.dtb.get(prefix) or self._load_record(prefix)
		
	def _load_record(self, prefix):
		record = Record(readfile(self.directory + prefix + '.txt'))
		self.dtb[prefix] = record
		return record