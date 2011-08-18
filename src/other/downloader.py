from common.io import savefile
from time import sleep

from urllib.request import urlopen
from preprocess.html_remover import HTMLRemover
from other.linksCollector import html_to_text
from collections import Counter

class Downloader:
	def download(self, urls, targetFolder):
		for url in urls:
			try:
				cont = urlopen(url).read().decode('utf-8')
				savefile(cont, targetFolder + self.getName(url))
				print('OK: ' + url)
				sleep(2)
			except Exception as err:
				print('Unable to get: ' + url)
				print('Error: ' + str(err))
				
	def getName(self, url):
		return url.replace('http://', '').replace('/', '_')
				
#getSites = Downloader().download
#getSites(('http://www.novinky.cz/domaci/' + str(i) + '-clanek.html' for i in range(6960, 10000)), '/Users/lukashavrlant/Desktop/wiki/')

url = 'http://localhost/jakpsatweb/pouzitelnost.html'
cont = urlopen(url).read().decode('utf-8')

funobj = HTMLRemover().compile


objver = funobj(cont)
funver = html_to_text(cont)

objCounter = Counter(objver.split())
funCounter = Counter(funver.split())

print(objCounter)
print('---------------------------------------')
print('---------------------------------------')
print('---------------------------------------')
print('---------------------------------------')
print('---------------------------------------')
print(funCounter)

print('ROZDÍLY')
print(objCounter - funCounter)
print(funCounter - objCounter)
