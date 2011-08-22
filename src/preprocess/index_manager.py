from common.io import download, savefile
from preprocess.index_builder import toIndex, getKeywords, getDocumentsInfo
from urllib.error import HTTPError
from other.constants import DOCUMENT_INFO_NAME, STEMSDICT_NAME,	KEYWORDSINDOCUMENTS_NAME
from retrieval.index import Index
import os
from common.czech_stemmer import wordCounter, savedStems
from common.string import strip_accents
from other.stopwatch import Stopwatch
import shelve

class IndexManager:
	
	def __init__(self):
		self.keylen = 1
		self.keywordsCount = 10
		self.keyScoreLimit = 35
		self.minKeywords = 3
		self.dynamicKeywords = True
		self.shutUp = True
		
	def build(self, urls, folder, stopwords):
		"Builds an index in 'folder'"
		watcher = Stopwatch()
		watcher.start()
		self._build(urls, folder, stopwords)
		watcher.elapsed('done')
		print(watcher)
		
	def _elapsed(self, status):
		if not self.shutUp:
			print(status)
		
			
	def _build(self, urls, folder, stopwords):
		indexFolder = folder + 'index/'
		infoFolder = folder + 'info/'
		
		sites, downloadedURL = self._downloadDocuments(urls)
		
		try:
			infoDtb = shelve.open(infoFolder + 'info') 
			self._elapsed('Creating index...')
			indexInfo = toIndex(sites, downloadedURL, stopwords, self.keylen, self._elapsed)
			self._createFolder([indexFolder, infoFolder])
			self._createIndex(indexInfo, indexFolder, infoFolder)
			
			self._elapsed('Creating documents info and keywords...')
			infoDtb[DOCUMENT_INFO_NAME] = self._getDocsInfo(indexInfo, folder, infoFolder)
			
			self._elapsed('Creating stems dictionary...')
			infoDtb[STEMSDICT_NAME] = self._getStemDict(self.totalKeywords)
			
			self._elapsed('Creating keywords in documents relation...')
			infoDtb[KEYWORDSINDOCUMENTS_NAME] = self._getKeywordsInfo(self.totalKeywords, indexInfo['parsedDocs'])
			
			infoDtb.close()
			self._elapsed('Done!')
		except IOError as err:
			print("I/O error: {0}".format(err))
			
	def _downloadDocuments(self, urls):
		distUrls = list(set(urls))
		
		sites = []
		downloadedURL = []
		
		for url in distUrls:
			try:
				self._elapsed('Downloading: ' + url)
				sites.append(download(url))
				downloadedURL.append(url)
			except HTTPError as err:
				print('Cannot download {0}'.format(err.filename))
				print("HTTP error: {0}".format(err))
			except Exception as err:
				print(err)
					
		return sites, downloadedURL
			
	def _getKeywordsInfo(self, keywords, documents):
		documents = [set(x) for x in documents]
		keywords = {x[0] for x in keywords}
		keywordsInDocuments = []
		for doc in documents:
			keywordsInDocument = set()
			for keyword in keywords:
				if keyword in doc:
					keywordsInDocument.add(keyword)
			keywordsInDocuments.append(keywordsInDocument)
			
		return {'inDocuments':keywordsInDocuments, 'keywords':keywords}
			
	def _getStemDict(self, keywords):
		stemsWords = {}
		keywords = {x[0] for x in keywords}
		
		for word, stem in savedStems.items():
			stem = strip_accents(stem)
			if stem in keywords:
				temp = stemsWords.get(stem, [])
				temp.append(word)
				stemsWords[stem] = temp
			
		for stem, words in stemsWords.items():
			stemsWords[stem] = max([(x, wordCounter[x]) for x in words], key=lambda x: x[1])[0]
			
		return stemsWords
	
	def _createFolder(self, folders):
		for folder in folders:
			if not os.path.exists(folder):
				os.makedirs(folder)
			
	def _createIndex(self, indexInfo, indexFolder, infoFolder):
		self._saveIndex(indexInfo['index'], indexFolder)
		#self._saveData(indexInfo['allwords'], infoFolder, ALL_WORDS_NAME)
			
	def _getDocsInfo(self, indexInfo, folder, infoFolder):
		documentsInfo = getDocumentsInfo(indexInfo)
		keywords = getKeywords(indexInfo['parsedDocs'], Index(folder, documentsInfo))
		totalKeywords = set()	
			
		for docInfo, allDocKeywords in zip(documentsInfo, keywords):
			if self.dynamicKeywords:
				topKeywords = [x for x in allDocKeywords if x[1] > self.keyScoreLimit]
				if len(topKeywords) < self.minKeywords:
					topKeywords = allDocKeywords[:self.minKeywords]
			else:
				topKeywords = allDocKeywords[:self.keywordsCount]
				
			docInfo['keywords'] = topKeywords
			totalKeywords = totalKeywords.union(topKeywords)
		
		#self._saveData(documentsInfo, infoFolder, DOCUMENT_INFO_NAME)
		self.totalKeywords = totalKeywords
		return documentsInfo
		
	
	def _saveIndex(self, index, dir):
		for prefix, data in index.items():
			dtb = shelve.open(dir + prefix)
			for steminfo in data:
				dtb[steminfo[0][0]] = steminfo[1]
			dtb.close()
			
		
	def _saveData(self, data, folder, name):
		savefile(repr(data), folder + name)