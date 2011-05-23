import re
def replace_single(text, strings, replacement):
	return re.sub('|'.join(strings), replacement, text)	

def replace_dict(text, dic):
	for k, v in dic.items():
		text = text.replace(k, v)
	return text