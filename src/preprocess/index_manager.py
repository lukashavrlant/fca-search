from common.io import downloads, savefile
from preprocess.index_builder import toIndex
from urllib.error import HTTPError
from other.constants import DOCUMENT_INFO_NAME, ALL_WORDS_NAME

class IndexManager:
	
	def __init__(self):
		self.keylen = 1
		
	def build(self, urls, directory, stopwords):
		"Builds an index in 'directory'"
		
		indexDir = directory + 'index/'
		infoDir = directory + 'info/'
		
		try:
			sites = downloads(urls)
			indexInfo = toIndex(sites, urls, stopwords, self.keylen)
			self._save_index(indexInfo['index'], indexDir)
			self._save_data(self._get_site_info(indexInfo), infoDir, DOCUMENT_INFO_NAME)
			self._save_data(indexInfo['allwords'], infoDir, ALL_WORDS_NAME)
		except HTTPError as err:
			print("HTTP error: {0}".format(err))
			print("Filename: " + err.filename)
		except IOError as err:
			print("I/O error: {0}".format(err))
			
			
	def _save_index(self, index, dir):
		for k, v in index.items():
			savefile(str(v), dir + k + '.txt')
		
	def _save_data(self, data, directory, name):
		savefile(repr(data), directory + name)
		
	def _get_site_info(self, info):
		arr = []
		for url, wordscount, id in zip(info['urls'], info['wordscount'], range(len(info['urls']))):
			dic = {'url':url, 'wordscount':wordscount, 'id':id}
			arr.append(dic)
		return arr