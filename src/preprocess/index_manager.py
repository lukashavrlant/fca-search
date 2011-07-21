from common.io import downloads
from preprocess.index_builder import toindex, save_index

class IndexManager:
	keylen = 1
	
	def build(self, urls, directory):
		sites = downloads(urls)
		index = toindex(sites, self.keylen)
		
		try:
			save_index(index, directory)
		except IOError as err:
			print("I/O error: {0}".format(err))
		
	
## download files
#urls = lmap(lambda x: 'http://localhost/fca/' + str(x) +  '.html', range(6))
#sites = downloads(urls)
#groups = toindex(sites)
#save_index(groups, database_dir)

#for prefix, record in groups.items():
#	savefile(repr(record), directory + prefix + '.txt')