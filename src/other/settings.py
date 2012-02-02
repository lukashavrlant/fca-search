from common.io import readfile
import json

class Settings():
	"""Settings for search engine"""
	def __init__(self, path):
		self.loadSettings(path)
	
	def loadSettings(self, path):
		text = readfile(path)
		self.settings = json.loads(text)

	def get(self, first, second = None):
		firstValue = self.settings[first]
		if second:
			return firstValue[second]
		else:
			return firstValue

	def getInt(self, first, second = None):
		return int(self.get(first, second))

	def getBool(self, namespace, key, default):
		try:
			return self.settings[namespace][key] == 'True'
		except Exception as e:
			return default

	def intGetter(self, namespace):
		return lambda key, default: int(self.settings[namespace].get(key, default))
		