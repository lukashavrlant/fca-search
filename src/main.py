from common.io import readfiles, downloads, savefiles, savefile, readfile, download
from preprocess import basics, html_remover
from preprocess.basics import Basics
from common.funcfun import lmap
from preprocess.html_remover import HTMLRemover


urls = ['http://www.havrlant.net/', 'http://www.inf.upol.cz/', 'http://www.seznam.cz/']
filenames = list(map(lambda x: '../files/' + str(x) + '.txt', range(len(urls))))
sites = downloads(urls)
striphtml = HTMLRemover()
sites = lmap(striphtml.compile, sites)

basics = Basics()
sites = lmap(basics.compile, sites)

savefiles(sites, filenames)