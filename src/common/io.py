from urllib.request import urlopen, urlretrieve
from common.funcfun import each, lmap
import codecs
import hashlib

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

def trySaveFile(content, path, charset = 'utf-8'):
	try:
		savefile(content, path, charset)
		return True
	except:
		return False
	
def downloadFile(url, destination):
	urlretrieve(url, destination)

def md5(fileName):
    md5 = hashlib.md5()
    fd = open(fileName,"rb")
    while True:
        buffer = fd.read(1024)
        md5.update(buffer)
        if len(buffer) < 1024:
            break
    fd.close()
    return md5.hexdigest()