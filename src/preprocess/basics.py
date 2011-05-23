from common.string import replace_single
import re
from common.funcfun import sreduce

class Basics:
	def compile(self, text):
		functions =[self.remove_newlines, self.remove_double_spaces]
		return sreduce(functions, text)
	
	def remove_double_spaces(self, text):
		return re.sub('[ ]+', ' ', text)
	
	def remove_newlines(self, text):
		return replace_single(text, ['\\n', '\\r', '\\t'], ' ')