from common.io import downloads, savefile
from preprocess.index_builder import toindex

class IndexManager:
	keylen = 1
	
	def build(self, urls, directory):
		"Builds an index in 'directory'"
		sites = downloads(urls)
		index = toindex(sites, self.keylen)
		
		try:
			self._save_index(index, directory)
			self._save_translation(urls, directory)
		except IOError as err:
			print("I/O error: {0}".format(err))
			
			
	def _save_index(self, index, dir):
		for k, v in index.items():
			savefile(str(v), dir + k + '.txt')
			
	def _save_translation(self, urls, directory):
		savefile(repr(urls), directory + 'translation.txt')