from common.string import replace_single
import re
from common.funcfun import sreduce

class Basics:
	def compile(self, text):
		functions =[self.remove_white_spaces]
		return sreduce(functions, text)
	
	def remove_white_spaces(self, text):
		return re.sub('\s+', ' ', text)