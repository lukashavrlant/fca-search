from other.constants import TEMP_FOLDER, PDFTOTEXT
from common.io import downloadFile, readfile
import xml.etree.ElementTree as etree
import os
from glob import glob
import shutil
from common.string import normalizePDF


class FileHandlers: 
	def PDF(self, url, enc = 'UTF-8'):
		tempfile = TEMP_FOLDER + "temp."
		pdfdest = tempfile + "pdf"
		txtdest = tempfile + "txt"
		downloadFile(url, pdfdest)
		os.system(PDFTOTEXT + "-enc " + enc + " " + pdfdest + " " + txtdest)
		txt = readfile(txtdest)
		txt = normalizePDF(txt)
		return txt
	
	def ODT(self, url):
		tempfile = TEMP_FOLDER + "temp."
		odtdest = tempfile + "odt"
		downloadFile(url, odtdest)
		os.system('unzip  -q -d ' + TEMP_FOLDER + ' ' + odtdest)
		tree = etree.parse(TEMP_FOLDER + "content.xml")
		root = tree.getroot() 
		text = self.getTextFromXML(root)
		return text
	
	def getTextFromXML(self, xml):
		text = [xml.text] if xml.text else []
		for el in list(xml):
			text.append(self.getTextFromXML(el))
		return " ".join(text)
	
	def cleanTempIfNes(self, extension):
		if extension in ('.pdf', '.odt'):
			self.cleanTemp()
	
	def cleanTemp(self):
		try:
			files = glob(TEMP_FOLDER + "*")
			for path in files:
				if os.path.isdir(path):
					shutil.rmtree(path)
				else:
					os.remove(path)
		except Exception:
			pass