from urllib.request import urlopen
from common.funcfun import each, lmap
import codecs

def download(site):
	return urlopen(site).read().decode('utf-8')

def downloads(sites):
	return list(map(download, sites))

def savefile(content, path, charset = 'utf-8'):
	file = open(path, 'wb')
	if charset:
		content = content.encode(charset)
	file.write(content)
	file.close()
	
def savefiles(contents, paths):
	each(savefile, contents, paths)

def readfile(path, charset = 'utf-8'):
	fileObj = codecs.open(path, "r", charset)
	u = fileObj.read() 
	fileObj.close()
	return u

def readfiles(paths):
	return lmap(readfile, paths)