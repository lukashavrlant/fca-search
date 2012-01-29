from common.io import download, downloadFile, readfile
from preprocess.index_builder import toIndex, getKeywords
from urllib.error import HTTPError
from other.constants import DOCUMENT_INFO_NAME, STEMSDICT_NAME,	KEYWORDSINDOCUMENTS_NAME,\
	CHMOD_INDEX, SCORES_TABLE, TEMP_FOLDER, PDFTOTEXT
from retrieval.index import Index
import os
from common.czech_stemmer import wordCounter, savedStems
from common.string import strip_accents
from other.stopwatch import Stopwatch
import shelve
import shutil
import xml.etree.ElementTree as etree
import glob
from xml.etree.ElementTree import XML

class IndexManager:
	
	def __init__(self):
		self.keylen = 1
		self.keywordsCount = 10
		self.keyScoreLimit = 35
		self.minKeywords = 1
		self.dynamicKeywords = True
		self.shutUp = True
		
	def rebuild(self, newLinks, folder, stopwords):
		index = Index(folder)
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
		print(watcher)
		
	def deleteFolder(self, path):
		try:
			shutil.rmtree(path)
		except:
			pass
		
	def _elapsed(self, status):
		if not self.shutUp:
			print(status)
			
	def _build(self, urls, folder, stopwords):
		indexFolder = folder + 'index/'
		infoFolder = folder + 'info/'
		
		sites = self._downloadDocuments(urls)
		
		try:
			self._createFolder([indexFolder, infoFolder])
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
			
			infoDtb.close()
			os.chmod(infoFolder + 'info.db', CHMOD_INDEX)
			self._elapsed('Done!')
		except IOError as err:
			print("I/O error: {0}".format(err))
			print("Filename: {0}".format(err.filename))
			
	def _downloadDocuments(self, urls):
		distUrls = list(set(urls))
		
		documents = []
		
		for url in distUrls:
			try:
				self._elapsed('Downloading: ' + url)
				extension = os.path.splitext(url)[1]

				if extension == '.pdf':
					document = {'type':'txt', 'content':self.handlePDF(url), 'url':url}
					documents.append(document)
					self.cleanTemp()
				elif extension == '.odt':
					document = {'type':'txt', 'content':self.handleODT(url), 'url':url}
					documents.append(document)
					self.cleanTemp()
				else:
					document = {'type':'html', 'content':download(url), 'url':url}
					documents.append(document)
			except HTTPError as err:
				print('Cannot download {0}'.format(err.filename))
				print("HTTP error: {0}".format(err))
			except Exception as err:
				print(err)
					
		return documents
	
	def handlePDF(self, url, enc = "UTF-8"):
		tempfile = TEMP_FOLDER + "temp."
		pdfdest = tempfile + "pdf"
		txtdest = tempfile + "txt"
		downloadFile(url, pdfdest)
		os.system(PDFTOTEXT + "-enc " + enc + " " + pdfdest + " " + txtdest)
		txt = readfile(txtdest)
		os.remove(pdfdest)
		os.remove(txtdest)
		return txt
	
	def handleODT(self, url):
		tempfile = TEMP_FOLDER + "temp."
		odtdest = tempfile + "odt"
		downloadFile(url, odtdest)
		os.system('unzip  -q -d ' + TEMP_FOLDER + ' ' + odtdest)
		tree = etree.parse(TEMP_FOLDER + "content.xml")
		root = tree.getroot() 
		text = self.getTextFromXML(root)
		return text
	
	def cleanTemp(self):
		files = glob.glob(TEMP_FOLDER + "*")
		for path in files:
			if os.path.isdir(path):
				shutil.rmtree(path)
			else:
				os.remove(path)
		
	def getTextFromXML(self, xml):
		text = [xml.text] if xml.text else []
		for el in list(xml):
			text.append(self.getTextFromXML(el))
		return " ".join(text)
			
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
		keywordsScore = getKeywords(documentsInfo, Index(folder, documentsInfo))
		totalKeywords = set()
			
		for docInfo, allDocKeywords in zip(documentsInfo, keywordsScore):
			if self.dynamicKeywords:
				topKeywords = [x for x in allDocKeywords if x[1] > self.keyScoreLimit]
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
					
		
	
	def _saveIndex(self, index, dir):
		for prefix, data in index.items():
			path = dir + prefix
			dtb = shelve.open(path)
			for steminfo in data:
				dtb[steminfo[0][0]] = steminfo[1]
			dtb.close()
			os.chmod(path + '.db', CHMOD_INDEX)