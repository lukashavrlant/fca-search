from common.io import downloads, savefile
from preprocess.index_builder import toindex
from urllib.error import HTTPError

class IndexManager:
	keylen = 1
	
	def build(self, urls, directory):
		"Builds an index in 'directory'"
		
		indexDir = directory + 'index/'
		infoDir = directory + 'info/'
		
		try:
			sites = downloads(urls)
			indexInfo = toindex(sites, urls, self.keylen)
			self._save_index(indexInfo['index'], indexDir)
			self._save_data(indexInfo['urls'], infoDir, 'translation.txt')
			self._save_data(indexInfo['allwords'], infoDir, 'allwords.txt')
		except HTTPError as err:
			print("HTTP error: {0}".format(err))
			print("Filename: " + err.filename)
		except IOError as err:
			print("I/O error: {0}".format(err))
			
			
	def _save_index(self, index, dir):
		for k, v in index.items():
			savefile(str(v), dir + k + '.txt')
			
	def _save_translation(self, urls, directory):
		savefile(repr(urls), directory + 'translation.txt')
		
	def _save_data(self, data, directory, name):
		savefile(repr(data), directory + name)