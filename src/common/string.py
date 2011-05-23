import re
from common.funcfun import lmap

def replace_single(text, strings, replacement):
	return re.sub('|'.join(lmap(re.escape, strings)), replacement, text)	

def replace_dict(text, dic):
	for k, v in dic.items():
		text = text.replace(k, v)
	return text