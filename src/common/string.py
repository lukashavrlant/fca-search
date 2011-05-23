import re
import unicodedata
import string

def replace_single(text, strings, replacement):
	return re.sub('|'.join(map(re.escape, strings)), replacement, text)	

def replace_dict(text, dic):
	for k, v in dic.items():
		text = text.replace(k, v)
	return text

def sjoin(lst):
	return ''.join(map(str, lst))

def isletter(char):
	if strip_accents(char).lower() in string.ascii_lowercase:
		return char
	else:
		return False

def strip_accents(s):
	return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))