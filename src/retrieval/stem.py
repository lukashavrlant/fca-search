from common.funcfun import lmap
class Stem:
	def __init__(self, line):
		self.stem = line
		self.name = line[0][0]
		self.totalcount = line[0][1]
		self.documents = line[1]
		self.docids = lmap(lambda x: x[0], self.documents) 