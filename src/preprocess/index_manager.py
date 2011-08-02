from common.io import downloads, savefile
from preprocess.index_builder import toIndex
from urllib.error import HTTPError
from other.constants import DOCUMENT_INFO_NAME, ALL_WORDS_NAME
from retrieval.index import Index
from retrieval.ranking import document_score
from preprocess.words import getstem
from common.funcfun import lmap

class IndexManager:
	
	def __init__(self):
		self.keylen = 1
		self.keywordsCount = 10
		
	def build(self, urls, directory, stopwords):
		"Builds an index in 'directory'"
		
		indexDir = directory + 'index/'
		infoDir = directory + 'info/'
		
		try:
			sites = downloads(urls)
			indexInfo = toIndex(sites, urls, stopwords, self.keylen)
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
		documentsInfo = self._getDocumentsInfo(indexInfo)
		keywords = self._getKeywords(indexInfo['parsedDocs'], Index(directory, documentsInfo))	
			
		for docInfo, allKeywords in zip(documentsInfo, keywords):
			topKeywords = lmap(lambda x: x[0], allKeywords)[:self.keywordsCount]
			docInfo['keywords'] = topKeywords
		
		self._saveData(documentsInfo, infoDir, DOCUMENT_INFO_NAME)
		
	def _getKeywords(self, documents, index):
		keywords = []
		for docID, content in enumerate(documents):
			keyValues = {}
			for word in content:
				stem = getstem(word)
				keyValues[stem] = document_score([stem], docID, index)
				
			foo = sorted(keyValues.items(), key=lambda x: x[1], reverse = True)
			keywords.append(foo)
		return keywords
		
	
	def _saveIndex(self, index, dir):
		for k, v in index.items():
			savefile(str(v), dir + k + '.txt')
		
	def _saveData(self, data, directory, name):
		savefile(repr(data), directory + name)
		
	def _getDocumentsInfo(self, info):
		arr = []
		for url, wordscount, id in zip(info['urls'], info['wordscount'], range(len(info['urls']))):
			dic = {'url':url, 'wordscount':wordscount, 'id':id}
			arr.append(dic)
		return arr