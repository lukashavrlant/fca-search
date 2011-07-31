from urllib.request import urlopen
from common.funcfun import each, lmap
import codecs

def download(site):
	return urlopen(site).read().decode('utf-8')

def downloads(sites):
	return list(map(download, sites))

def savefile(content, path):
	file = open(path, 'wb')
	file.write(content.encode('utf-8'))
	file.close()
	
def savefiles(contents, paths):
	each(savefile, contents, paths)

def readfile(path):
	fileObj = codecs.open(path, "r", "utf-8")
	u = fileObj.read() 
	fileObj.close()
	return u

def readfiles(paths):
	return lmap(readfile, paths)