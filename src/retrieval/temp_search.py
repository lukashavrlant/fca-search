from preprocess.index_builder import toIndex, getKeywords
from common.funcfun import nothing
from retrieval.index_proxy import IndexProxy
from preprocess.index_manager import IndexManager
from other.settings import Settings
from other.constants import *

class TempSearch:
	def __init__(self):
		self.keylen = 1
		self.manager = IndexManager(Settings())
		self.dynamicKeywords = True
		self.maxKeywords = 2
		self.minKeywords = 1

	def build(self, documents, stopwords):
		infoDtb = {}
		options = documents.get('options', {})
		lang = options.get('lang', 'cs')
		documentsData = documents['data']

		if not documentsData:
			raise Exception('No documents downloaded')

		indexInfo = toIndex(documentsData, stopwords, self.keylen, lang)
		self.indexProxy = IndexProxy()
		self.indexProxy.setIndexInfo(indexInfo)
		metadata, scoresTable = self.getDocsInfo(indexInfo, lang)
	
		stemsDict = self.manager._getStemDict(self.totalKeywords)
		keywordsInDocuments = self.manager._getKeywordsInfo(self.totalKeywords, [x['content'] for x in indexInfo['documents']])
		
		self.manager.findDescription(metadata, indexInfo['documents'], lang)

		infoDtb[SCORES_TABLE] = scoresTable
		infoDtb[STEMSDICT_NAME] = stemsDict
		infoDtb[KEYWORDSINDOCUMENTS_NAME] = keywordsInDocuments
		infoDtb['allwords'] = indexInfo['allRealWords']
		infoDtb[DOCUMENT_INFO_NAME] = metadata
		self.indexProxy.setInfoDtb(infoDtb)
		return self.indexProxy
		

	

	def getDocsInfo(self, indexInfo, lang):
		documentsInfo = indexInfo['documents']
		keywordsScore = getKeywords(documentsInfo, self.indexProxy, nothing, lang)
		totalKeywords = set()
		realLimit = self.manager.countKeywordsLimit(keywordsScore)
			
		for docInfo, allDocKeywords in zip(documentsInfo, keywordsScore):
			if self.dynamicKeywords:
				topKeywords = [x for x in allDocKeywords if x[1] > realLimit][:self.maxKeywords]
				if len(topKeywords) < self.minKeywords:
					topKeywords = allDocKeywords[:self.minKeywords]
			else:
				topKeywords = allDocKeywords[:self.keywordsCount]
				
			docInfo['keywords'] = topKeywords
			totalKeywords = totalKeywords.union(topKeywords)
		
		self.totalKeywords = totalKeywords
		totalKeywordsName = [x[0] for x in totalKeywords]
		
		scoresTable = self.manager._getKeywordsScoreTable(keywordsScore, totalKeywordsName)
		
		newDocInfo = []
		
		for docInfo in documentsInfo:
			d = {}
			for key in ['title', 'url', 'keywords', 'words', 'id', 'description']:
				d[key] = docInfo[key]
			newDocInfo.append(d)
		
		return newDocInfo, scoresTable