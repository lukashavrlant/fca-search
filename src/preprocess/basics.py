from common.string import replace_single
import re
import string
from common.funcfun import sreduce
import unicodedata

class Basics:
	def compile(self, text):
		functions = [self.remove_punctuation, self.remove_white_spaces, self.strip_accents,
					lambda x: x.lower(), lambda x: x.strip()]
		return sreduce(functions, text)
	
	def remove_white_spaces(self, text):
		return re.sub('\s+', ' ', text)
	
	def remove_punctuation(self, text):
		return replace_single(text, list(string.punctuation), ' ')
	
	def strip_accents(self, s):
		return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))