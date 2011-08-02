from common.io import downloads, savefile
from preprocess.index_builder import toIndex, getKeywords, getDocumentsInfo
from urllib.error import HTTPError
from other.constants import DOCUMENT_INFO_NAME, ALL_WORDS_NAME
from retrieval.index import Index
from common.funcfun import lmap

class IndexManager:
	
	def __init__(self):
		self.keylen = 1
		self.keywordsCount = 10
		
	def build(self, urls, directory, stopwords):
		"Builds an index in 'directory'"
		
		indexDir = directory + 'index/'
		infoDir = directory + 'info/'
		
		distUrls = list(set(urls))
		
		try:
			sites = downloads(distUrls)
			indexInfo = toIndex(sites, distUrls, stopwords, self.keylen)
			self._createIndex(indexInfo, indexDir, infoDir)
			self._saveDocsInfo(indexInfo, directory, infoDir)
		except HTTPError as err:
			print("HTTP error: {0}".format(err))
			print("Filename: " + err.filename)
		except IOError as err:
			print("I/O error: {0}".format(err))
			
	def _createIndex(self, indexInfo, indexDir, infoDir):
		self._saveIndex(indexInfo['index'], indexDir)
		self._saveData(indexInfo['allwords'], infoDir, ALL_WORDS_NAME)
			
	def _saveDocsInfo(self, indexInfo, directory, infoDir):
		documentsInfo = getDocumentsInfo(indexInfo)
		keywords = getKeywords(indexInfo['parsedDocs'], Index(directory, documentsInfo))	
			
		for docInfo, allKeywords in zip(documentsInfo, keywords):
			topKeywords = lmap(lambda x: x[0], allKeywords)[:self.keywordsCount]
			docInfo['keywords'] = topKeywords
		
		self._saveData(documentsInfo, infoDir, DOCUMENT_INFO_NAME)
		
	
	def _saveIndex(self, index, dir):
		for k, v in index.items():
			savefile(str(v), dir + k + '.txt')
		
	def _saveData(self, data, directory, name):
		savefile(repr(data), directory + name)