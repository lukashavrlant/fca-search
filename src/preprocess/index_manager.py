from common.io import download
from preprocess.index_builder import toIndex, getKeywords
from urllib.error import HTTPError
from other.constants import DOCUMENT_INFO_NAME, STEMSDICT_NAME,	KEYWORDSINDOCUMENTS_NAME,\
	CHMOD_INDEX, SCORES_TABLE, TEMP_FOLDER, SETTINGS_FILE, INDEX_FOLDER_NAME, INFO_FOLDER_NAME
from retrieval.index import Index
import os
from common.czech_stemmer import wordCounter, savedStems
from common.string import strip_accents
from other.stopwatch import Stopwatch
import shelve
import shutil
from preprocess.file_handlers import FileHandlers

class IndexManager:
	
	def __init__(self, settings):
		self.settings = settings
		self.applySettings(settings)
		self.shutUp = True
		
	def rebuild(self, newLinks, folder, stopwords):
		index = Index(folder, self.settings)
		oldLinks = index.getLinks()
		links = list(set(newLinks) | set(oldLinks))
		self.build(links, folder, stopwords)
		
	def build(self, urls, folder, stopwords):
		"Builds an index in 'folder'"
		self.deleteFolder(folder)
		watcher = Stopwatch()
		watcher.start()
		self._build(urls, folder, stopwords)
		watcher.elapsed('done')
		# print(watcher)

	def applySettings(self, settings):
		namespace = 'index'
		getter = settings.intGetter(namespace)
		self.keylen = getter('keylen', 1)
		self.keywordsCount = getter('keywordsCount', 10)
		self.keyScoreLimit = getter('keyScoreLimit', 35)
		self.minKeywords = getter('minKeywords', 1)
		self.maxKeywords = getter('maxKeywords', 10)
		self.dynamicKeywords = settings.getBool(namespace, 'dynamicKeywords', True)
		self.unsupportedFiles = {'.'+x for x in {'doc', 'zip', 'png', 'jpg', 'gif', 'gz'}}
		
	def deleteFolder(self, path):
		try:
			shutil.rmtree(path)
		except:
			pass
		
	def _elapsed(self, status):
		if not self.shutUp:
			print(status)
			
	def _build(self, urls, folder, stopwords):
		indexFolder = folder + INDEX_FOLDER_NAME
		infoFolder = folder + INFO_FOLDER_NAME
		
		try:
			self._createFolder([indexFolder, infoFolder, TEMP_FOLDER])
			sites = self._downloadDocuments(urls)
			infoDtb = shelve.open(infoFolder + 'info') 
			indexInfo = toIndex(sites, stopwords, self.keylen, self._elapsed)
			self._createIndex(indexInfo, indexFolder, infoFolder)
			
			self._elapsed('Creating documents info and keywords...')
			metadata, scoresTable = self._getDocsInfo(indexInfo, folder, infoFolder)
			
			infoDtb[DOCUMENT_INFO_NAME] = metadata 
			infoDtb[SCORES_TABLE] = scoresTable
			
			self._elapsed('Creating stems dictionary...')
			infoDtb[STEMSDICT_NAME] = self._getStemDict(self.totalKeywords)
			
			self._elapsed('Creating keywords in documents relation...')
			infoDtb[KEYWORDSINDOCUMENTS_NAME] = self._getKeywordsInfo(self.totalKeywords, [x['content'] for x in indexInfo['documents']])
			
			infoDtb['allwords'] = indexInfo['allRealWords']

			infoDtb.close()
			os.chmod(infoFolder + 'info.db', CHMOD_INDEX)

			self.settings.save(folder + SETTINGS_FILE)
			self._elapsed('Done!')
		except IOError as err:
			print("I/O error: {0}".format(err))
			print("Filename: {0}".format(err.filename))

	def filterURL(self, urls):
		filtered = {x for x in urls if os.path.splitext(x)[1] not in self.unsupportedFiles}
		return sorted(filtered)

			
	def _downloadDocuments(self, urls):
		distUrls = self.filterURL(urls)
		documents = []
		handle = FileHandlers()
		
		for url in distUrls:
			try:
				self._elapsed('Downloading: ' + url)
				extension = os.path.splitext(url)[1]

				if extension == '.pdf':
					document = {'type':'txt', 'content':handle.PDF(url), 'url':url}
				elif extension == '.odt':
					document = {'type':'txt', 'content':handle.ODT(url), 'url':url}
				else:
					document = {'type':'html', 'content':download(url), 'url':url}
					
				documents.append(document)
			except HTTPError as err:
				print('Cannot download {0}'.format(err.filename))
				print("HTTP error: {0}".format(err))
			except Exception as err:
				print(err)
				
			handle.cleanTempIfNes(extension)
					
		return documents
			
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
			
	def _getDocsInfo(self, indexInfo, folder, infoFolder):
		documentsInfo = indexInfo['documents']
		keywordsScore = getKeywords(documentsInfo, Index(folder, self.settings, documentsInfo))
		totalKeywords = set()
			
		for docInfo, allDocKeywords in zip(documentsInfo, keywordsScore):
			if self.dynamicKeywords:
				topKeywords = [x for x in allDocKeywords if x[1] > self.keyScoreLimit][:self.maxKeywords]
				if len(topKeywords) < self.minKeywords:
					topKeywords = allDocKeywords[:self.minKeywords]
			else:
				topKeywords = allDocKeywords[:self.keywordsCount]
				
			docInfo['keywords'] = topKeywords
			totalKeywords = totalKeywords.union(topKeywords)
		
		self.totalKeywords = totalKeywords
		totalKeywordsName = [x[0] for x in totalKeywords]
		
		scoresTable = self._getKeywordsScoreTable(keywordsScore, totalKeywordsName)
		
		newDocInfo = []
		
		for docInfo in documentsInfo:
			d = {}
			for key in ['title', 'url', 'keywords', 'words', 'id', 'description']:
				d[key] = docInfo[key]
			newDocInfo.append(d)
		
		return newDocInfo, scoresTable
	
	def _getKeywordsScoreTable(self, keywordsScore, allKeywords):
		table = []
		allKeywords = set(allKeywords)
		
		for docKeywords in keywordsScore:
			table.append({k:v for k,v in docKeywords if k in allKeywords})

		return table
					
		
	
	def _saveIndex(self, index, directory):
		for prefix, data in index.items():
			path = directory + prefix
			dtb = shelve.open(path)
			for steminfo in data:
				dtb[steminfo[0][0]] = steminfo[1]
			dtb.close()
			os.chmod(path + '.db', CHMOD_INDEX)