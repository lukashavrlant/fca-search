from common.io import downloads, savefile
from preprocess.index_builder import toindex
from urllib.error import HTTPError

class IndexManager:
	keylen = 1
	
	def build(self, urls, directory):
		"Builds an index in 'directory'"
		try:
			sites = downloads(urls)
			index = toindex(sites, self.keylen)
			self._save_index(index, directory)
			self._save_translation(urls, directory)
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