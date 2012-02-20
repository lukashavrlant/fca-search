from common.io import readfile, savefile
import json

class Settings():
	"""Settings for search engine"""
	def __init__(self, path):
		self.loadSettings(path)
	
	def loadSettings(self, path):
		self.text = readfile(path)
		self.settings = json.loads(self.text)

	def save(self, path):
		savefile(self.text, path)

	def get(self, key):
		return self.settings.get(key, defaultValues[key])

	def getDefaultValue(self, key):
		return defaultValues[key]

		
defaultValues = {
		"keylen" : 1,
		"keywordsCount" : 10,
		"keyScoreLimit" : 35,
		"minKeywords" : 1,
		"dynamicKeywords" : True,
		"maxKeywords" : 10,
		"maxDocumentsInContext" : 50,
		"maxKeywordsPerDocument" : 5
}