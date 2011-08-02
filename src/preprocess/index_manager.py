from common.io import downloads, savefile
from preprocess.index_builder import toIndex, getKeywords, getDocumentsInfo
from urllib.error import HTTPError
from other.constants import DOCUMENT_INFO_NAME, ALL_WORDS_NAME
from retrieval.index import Index
from common.funcfun import lmap
import os

class IndexManager:
	
	def __init__(self):
		self.keylen = 1
		self.keywordsCount = 10
		
	def build(self, urls, folder, stopwords):
		"Builds an index in 'folder'"
		
		indexFolder = folder + 'index/'
		infoFolder = folder + 'info/'
		
		distUrls = list(set(urls))
		
		try:
			sites = downloads(distUrls)
			indexInfo = toIndex(sites, distUrls, stopwords, self.keylen)
			self._createFolder([indexFolder, infoFolder])
			self._createIndex(indexInfo, indexFolder, infoFolder)
			self._saveDocsInfo(indexInfo, folder, infoFolder)
		except HTTPError as err:
			print("HTTP error: {0}".format(err))
			print("Filename: " + err.filename)
		except IOError as err:
			print("I/O error: {0}".format(err))
	
	def _createFolder(self, folders):
		for folder in folders:
			if not os.path.exists(folder):
				os.makedirs(folder)
			
	def _createIndex(self, indexInfo, indexFolder, infoFolder):
		self._saveIndex(indexInfo['index'], indexFolder)
		self._saveData(indexInfo['allwords'], infoFolder, ALL_WORDS_NAME)
			
	def _saveDocsInfo(self, indexInfo, folder, infoFolder):
		documentsInfo = getDocumentsInfo(indexInfo)
		keywords = getKeywords(indexInfo['parsedDocs'], Index(folder, documentsInfo))	
			
		for docInfo, allKeywords in zip(documentsInfo, keywords):
			topKeywords = lmap(lambda x: x[0], allKeywords)[:self.keywordsCount]
			docInfo['keywords'] = topKeywords
		
		self._saveData(documentsInfo, infoFolder, DOCUMENT_INFO_NAME)
		
	
	def _saveIndex(self, index, dir):
		for k, v in index.items():
			savefile(str(v), dir + k + '.txt')
		
	def _saveData(self, data, folder, name):
		savefile(repr(data), folder + name)