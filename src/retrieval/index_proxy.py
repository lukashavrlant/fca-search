from retrieval.index import Index
from retrieval.stem import Stem
from other.constants import *

class IndexProxy(Index):
	def __init__(self):
		self.index = None
		self.info = None

		self.stemsDict = None
		self.docKeywords = None
		self.allKeywords = None
		self.searchedStem = {}

	def setIndexInfo(self, indexInfo):
		self.index = indexInfo
		self.total_records = len(indexInfo['documents'])

	def setInfoDtb(self, info):
		self.info = info
		self.documents_info = info[DOCUMENT_INFO_NAME]

	def get_stem_info(self, stem):
		index = self.index['index']
		line = index[stem[:1]]
		for stemInfo in line:
			if stemInfo[0][0] == stem:
				return Stem(stemInfo[1], stem)

		raise Exception('Cannot find stem ' + stem)

