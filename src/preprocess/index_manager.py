from common.io import download, savefile
from preprocess.index_builder import toIndex, getKeywords, getDocumentsInfo
from urllib.error import HTTPError
from other.constants import DOCUMENT_INFO_NAME, ALL_WORDS_NAME
from retrieval.index import Index
import os

class IndexManager:
	
	def __init__(self):
		self.keylen = 1
		self.keywordsCount = 10
		self.keyScoreLimit = 35
		self.minKeywords = 3
		self.dynamicKeywords = True
		
	def build(self, urls, folder, stopwords):
		"Builds an index in 'folder'"
		
		indexFolder = folder + 'index/'
		infoFolder = folder + 'info/'
		
		distUrls = list(set(urls))
		
		try:
			#sites = downloads(distUrls)
			sites = []
			downloadedURL = []
			
			for url in distUrls:
				try:
					sites.append(download(url))
					downloadedURL.append(url)
				except HTTPError as err:
						print('Cannot download {0}'.format(err.filename))
						print("HTTP error: {0}".format(err))
			
			indexInfo = toIndex(sites, downloadedURL, stopwords, self.keylen)
			self._createFolder([indexFolder, infoFolder])
			self._createIndex(indexInfo, indexFolder, infoFolder)
			self._saveDocsInfo(indexInfo, folder, infoFolder)
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
			if self.dynamicKeywords:
				topKeywords = [x for x in allKeywords if x[1] > self.keyScoreLimit]
				if len(topKeywords) < self.minKeywords:
					topKeywords = allKeywords[:self.minKeywords]
			else:
				topKeywords = allKeywords[:self.keywordsCount]
				
			docInfo['keywords'] = topKeywords
		
		self._saveData(documentsInfo, infoFolder, DOCUMENT_INFO_NAME)
		
	
	def _saveIndex(self, index, dir):
		for k, v in index.items():
			savefile(str(v), dir + k + '.txt')
		
	def _saveData(self, data, folder, name):
		savefile(repr(data), folder + name)