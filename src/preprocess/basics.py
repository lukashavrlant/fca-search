from common.string import isletter, sjoin, remove_white_spaces
from common.funcfun import sreduce

class Basics:
	def compile(self, text):
		functions = [self.remove_nonletters, self.remove_white_spaces, 
					lambda x: x.lower(), lambda x: x.strip()]
		return sreduce(functions, text)
	
	def remove_white_spaces(self, text):
		return remove_white_spaces(text)
	
	def remove_nonletters(self, text):
		return sjoin(map(lambda x: isletter(x) or ' ', text))