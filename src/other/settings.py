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
		try:
			return self.settings[key]
		except Exception as e:
			return defaultValues[key]

	def set(self, key, value):
		try:
			self.settings[key] = int(value)
		except Exception:
			self.settings[key] = value

		self.text = json.dumps(self.settings)

defaultValues = {
		"keylen" : 1,
		"keywordsCount" : 10,
		"keyScoreLimit" : 35,
		"minKeywords" : 1,
		"dynamicKeywords" : True,
		"maxKeywords" : 10,
		"disallowExtensions" : ["doc", "zip", "png", "jpg", "gif", "gz", "ico", "rtf"],
		"maxDocumentsInContext" : 50,
		"maxKeywordsPerDocument" : 5,
		"charset" : 'utf-8',
		"lang" : 'cs',
		"forceDesc" : False
}