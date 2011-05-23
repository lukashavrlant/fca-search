from common.string import isletter, sjoin
import re
from common.funcfun import sreduce, lmap

class Basics:
	def compile(self, text):
		functions = [self.remove_nonletters, self.remove_white_spaces, 
					lambda x: x.lower(), lambda x: x.strip()]
		return sreduce(functions, text)
	
	def remove_white_spaces(self, text):
		return re.sub('\s+', ' ', text)
	
	def remove_nonletters(self, text):
		return sjoin(lmap(lambda x: isletter(x) or ' ', text))