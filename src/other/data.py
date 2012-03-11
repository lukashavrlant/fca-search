from other.constants import DATA_FOLDER, STOPWORDS_NAME
from common.io import readfile

_data = {}

def getStopWords(lang):
	return _cache_result('stopwords', lambda: readfile(DATA_FOLDER + STOPWORDS_NAME + "." + lang + ".txt").split() + list('abcdefghijklmnopqrstuvwxyz'))
	
def _cache_result(key, getValue):
	try:
		return _data[key]
	except Exception:
		_data[key] = getValue()
		return _data[key]