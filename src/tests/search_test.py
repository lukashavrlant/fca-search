import unittest
from other.constants import PYTHON3, ROOT_FOLDER
from retrieval.search_engine import SearchEngine
from other.constants import TEST_FOLDER
from other.data import getStopWords
from common.io import readfile, savefile
from retrieval.index import Index
from subprocess import Popen, PIPE
from json import loads
from other.interface import searchQuery

class SearchTest(unittest.TestCase):
	def testSearchCommand(self):
		path = TEST_FOLDER 
		fun = self.runShell
		dfun = lambda dtb, q: fun(dtb, q).decode("utf-8")
		save = lambda cont, name: savefile(cont, path + name + '.txt', False)
		read = lambda name: readfile(path + name + '.txt')
		ass = self.assertEqual
		
		# search matweb
		queries = ['derivace', 'nesmysl', '(spocetne OR nespocetne) mnoziny', 'rovnice', 'rovnice NOT (linearni OR pravdepodobnost)']

		ass(dfun('matweb-test', 'derivace'), read('matweb0'))
		ass(dfun('matweb-test', 'nesmysl'), read('matweb1'))
		ass(dfun('matweb-test', '(spocetne OR nespocetne) mnoziny'), read('matweb2'))
		# ass(dfun('matweb-test', 'rovnice'), read('matweb3'))
		ass(dfun('matweb-test', 'rovnice NOT (linearni OR pravdepodobnost)'), read('matweb4'))

		# for num, q in enumerate(queries):
		# 	filename = 'matweb' + str(num)
		# 	save(fun('matweb', q), filename)

	def test_SEresults(self):
		ass = self.assertEqual
		fun = lambda q: searchQuery('matweb-test', q)['origin']
		# print(fun('(množiny NOT (spočetné OR prvek)) AND faktoriál'))

		ass(fun('derivace'), {'wordsTerms': ['derivace'], 'documents': [{'description': '', 'title': 'Derivace funkce — Matematika polopatě', 'url': 'http://www.matweb.cz/derivace', 'score': 413.26129887178485, 'words': 1156, 'keywords': [('tecn', 125.01317), ('derivak', 103.31532), ('smernik', 99.14838), ('secn', 55.04341), ('bod', 38.57972), ('tangens', 37.78559)], 'id': 14}, {'description': '', 'title': 'Úvodní příklady na derivace — Matematika polopatě', 'url': 'http://www.matweb.cz/derivace-priklady', 'score': 321.4254546780549, 'words': 687, 'keywords': [('derivak', 80.35636)], 'id': 16}, {'description': '', 'title': 'Pokročilé příklady na derivace — Matematika polopatě', 'url': 'http://www.matweb.cz/derivace-pokrocile-priklady', 'score': 165.30451954871393, 'words': 501, 'keywords': [('derivak', 41.32613)], 'id': 15}, {'description': '', 'title': 'Průběh funkce — Matematika polopatě', 'url': 'http://www.matweb.cz/prubeh-funkce', 'score': 96.42763640341646, 'words': 1757, 'keywords': [('tecn', 206.91836), ('konvexn', 101.83525), ('derivak', 96.42764), ('bod', 92.06525), ('ext', 81.90518), ('konkavn', 57.88243), ('maximum', 57.81936), ('inflexn', 51.72959), ('lokaln', 51.72959), ('rostouc', 45.92314)], 'id': 102}, {'description': '', 'title': 'Vzorce pro práci s derivacemi — Matematika polopatě', 'url': 'http://www.matweb.cz/derivace-vzorce', 'score': 82.65225977435696, 'words': 127, 'keywords': [('derivak', 20.66306)], 'id': 17}, {'description': '', 'title': 'Kategorie: Analýza — Matematika polopatě', 'url': 'http://www.matweb.cz/kategorie-analyza', 'score': 27.550753258118988, 'words': 218, 'keywords': [('derivak', 27.55075)], 'id': 42}, {'description': '', 'title': 'Spojitost funkce — Matematika polopatě', 'url': 'http://www.matweb.cz/spojitost-funkce', 'score': 11.479480524216246, 'words': 693, 'keywords': [('spojit', 102.78998), ('nespojitost', 86.21598), ('limit', 70.94667), ('bod', 49.97828), ('spojitost', 39.09077)], 'id': 119}, {'description': '', 'title': 'Limita posloupnosti — Matematika polopatě', 'url': 'http://www.matweb.cz/limita-posloupnosti', 'score': 9.183584419372997, 'words': 1195, 'keywords': [('limit', 146.62312), ('posloupnost', 140.13391), ('epsilon', 54.67468), ('clen', 39.13064)], 'id': 64}, {'description': '', 'title': 'Posloupnosti — Matematika polopatě', 'url': 'http://www.matweb.cz/posloupnosti', 'score': 9.183584419372997, 'words': 1068, 'keywords': [('posloupnost', 156.94998), ('diferenk', 55.04341), ('aritmetick', 47.02948), ('clen', 39.13064)], 'id': 93}, {'description': '', 'title': 'Limita funkce — Matematika polopatě', 'url': 'http://www.matweb.cz/limita-funkce', 'score': 9.183584419372997, 'words': 1731, 'keywords': [('limit', 201.01556), ('okol', 123.00017), ('funkcn', 67.53403), ('bod', 62.25365), ('hromadn', 56.04039), ('epsilon', 50.76934), ('delt', 45.03552), ('bliz', 39.75447), ('hranik', 38.79719)], 'id': 63}, {'description': '', 'title': 'Matematické nástroje — Matematika polopatě', 'url': 'http://www.matweb.cz/nastroje', 'score': 6.887688314529747, 'words': 462, 'keywords': [('wolfram', 30.17559)], 'id': 77}, {'description': '', 'title': 'Všechny změny — Matematika polopatě', 'url': 'http://www.matweb.cz/vsechny-zmeny', 'score': 4.591792209686498, 'words': 878, 'keywords': [('pridan', 44.12861), ('ledn', 40.03157), ('listopad', 35.02762)], 'id': 140}, {'description': '', 'title': 'Vlastnosti funkce — Matematika polopatě', 'url': 'http://www.matweb.cz/funkce', 'score': 4.591792209686498, 'words': 1188, 'keywords': [('omezen', 51.32586), ('graf', 51.25292), ('maximum', 41.75843), ('minimum', 35.33406), ('shor', 35.33406)], 'id': 28}, {'description': '', 'title': 'Matematika polopatě — pro základní, střední a vysoké školy', 'url': 'http://www.matweb.cz/uvod', 'score': 2.295896104843249, 'words': 281, 'keywords': [('web', 26.06051)], 'id': 134}, {'description': '', 'title': 'Matematické symboly — Matematika polopatě', 'url': 'http://www.matweb.cz/symboly', 'score': 2.295896104843249, 'words': 521, 'keywords': [('symbol', 21.91071)], 'id': 122}], 'terms': ['derivak'], 'parsedQuery': 'derivak', 'pureQuery': 'derivace'})
		ass(str(fun('Rozdíl mezi mocninou a odmocninou')), "{'wordsTerms': ['Rozdíl', 'mocninou', 'odmocninou'], 'documents': [{'description': '', 'title': 'Pythagorova věta — Matematika polopatě', 'url': 'http://www.matweb.cz/pythagorova-veta', 'score': 16.825982976208675, 'words': 792, 'keywords': [('delk', 68.38983), ('ctverk', 51.98661), ('prepon', 49.71658), ('odvesn', 36.48738)], 'id': 104}, {'description': '', 'title': 'Co je to funkce — Matematika polopatě', 'url': 'http://www.matweb.cz/co-je-to-funkce', 'score': 15.944747199681863, 'words': 1782, 'keywords': [('vstup', 88.25722), ('vystup', 72.35304), ('parametr', 47.29778), ('argument', 37.83822), ('vrat', 35.09406), ('autom', 35.02762)], 'id': 9}, {'description': '', 'title': 'Komplexní čísla — Matematika polopatě', 'url': 'http://www.matweb.cz/komplexni-cisla', 'score': 11.234869895300925, 'words': 531, 'keywords': [('komplexn', 59.30171)], 'id': 52}, {'description': '', 'title': 'Kategorie: Čísla — Matematika polopatě', 'url': 'http://www.matweb.cz/kategorie-cisla', 'score': 7.213715915853486, 'words': 243, 'keywords': [('urok', 12.35704)], 'id': 43}, {'description': '', 'title': 'Goniometrické funkce — Matematika polopatě', 'url': 'http://www.matweb.cz/goniometrie', 'score': 7.089428941179831, 'words': 885, 'keywords': [('odvesn', 58.94116), ('uhl', 54.77677), ('delk', 40.0016), ('cosin', 39.09077), ('prepon', 38.01856)], 'id': 32}], 'terms': ['rozdil', 'mocn', 'odmocn'], 'parsedQuery': ('rozdil' AND 'mocn' AND 'odmocn'), 'pureQuery': 'Rozdíl mezi mocninou a odmocninou'}")
		ass(str(fun('(množiny NOT (spočetné OR prvek)) AND faktoriál')), "{'wordsTerms': ['množiny', 'faktoriál'], 'documents': [{'description': '', 'title': 'Faktoriál — Matematika polopatě', 'url': 'http://www.matweb.cz/faktorial', 'score': 150.63164566405294, 'words': 200, 'keywords': [('faktorial', 36.90246)], 'id': 26}, {'description': '', 'title': 'Matematické symboly — Matematika polopatě', 'url': 'http://www.matweb.cz/symboly', 'score': 13.215638230933573, 'words': 521, 'keywords': [('symbol', 21.91071)], 'id': 122}, {'description': '', 'title': 'Co je to funkce — Matematika polopatě', 'url': 'http://www.matweb.cz/co-je-to-funkce', 'score': 8.118721243258987, 'words': 1782, 'keywords': [('vstup', 88.25722), ('vystup', 72.35304), ('parametr', 47.29778), ('argument', 37.83822), ('vrat', 35.09406), ('autom', 35.02762)], 'id': 9}, {'description': '', 'title': 'Prvočísla — Matematika polopatě', 'url': 'http://www.matweb.cz/prvocisla', 'score': 5.192537217473644, 'words': 411, 'keywords': [('prvocisl', 45.90969)], 'id': 103}, {'description': '', 'title': 'Hlavolamy — Matematika polopatě', 'url': 'http://www.matweb.cz/hlavolamy', 'score': 3.6816350896814436, 'words': 607, 'keywords': [('alik', 75.05919), ('fotk', 45.03552), ('postak', 40.03157), ('bob', 35.02762), ('medved', 35.02762)], 'id': 33}, {'description': '', 'title': 'Absolutní hodnota — Matematika polopatě', 'url': 'http://www.matweb.cz/absolutni-hodnota', 'score': 2.9261840257853433, 'words': 172, 'keywords': [('absolutn', 16.1557)], 'id': 0}, {'description': '', 'title': 'Matematické nástroje — Matematika polopatě', 'url': 'http://www.matweb.cz/nastroje', 'score': 2.9261840257853433, 'words': 462, 'keywords': [('wolfram', 30.17559)], 'id': 77}], 'terms': ['mnoh', 'faktorial'], 'parsedQuery': (('mnoh' AND NOT(('spocetn' OR 'prvek'))) AND 'faktorial'), 'pureQuery': '(množiny NOT (spočetné OR prvek)) AND faktoriál'}")

	def test_spellcheck(self):
		ass = self.assertEqual
		fun = lambda q: searchQuery('matweb-test', q)['suggestions'][q]

		ass(fun('poslounposti'), 'posloupnosti')
		ass(fun('derivcae'), 'derivace')
		ass(fun('nemsysl'), 'nesmysl')
		ass(fun('hroamdny'), 'hromadny')


	def test_Generalization(self):
		ass = self.assertEqual
		fun = lambda q: searchQuery('matweb-test', q)['generalization']

		ass(fun('inverzni mnoziny prvky'), [{'words': ['inverzni'], 'rank': 24}, {'words': ['prvky'], 'rank': 20}, {'words': ['mnoziny'], 'rank': 19}])
		ass(fun('derivace'), [])
		ass(fun('bod hokus'), [{'words': ['hokus'], 'rank': 1}])

	def test_Specialization(self):
		ass = self.assertEqual
		fun = lambda q: searchQuery('matweb-test', q)['specialization']

		ass(fun('derivace'), [{'rank': 13, 'words': ['limita']}, {'rank': 12, 'words': ['posloupnosti']}, {'rank': 10, 'words': ['bodě']}, {'rank': 3, 'words': ['symboly']}])
		ass(fun('Pravděpodobnost OR množiny'), [{'rank': 6, 'words': ['hesla']}, {'rank': 5, 'words': ['lidí']}, {'rank': 4, 'words': ['kostce']}])
		ass(fun('kravina'), [])

	def test_Siblings(self):
		ass = self.assertEqual
		fun = lambda q: searchQuery('matweb-test', q)['siblings']

		ass(fun('derivace'), [])
		ass(fun('limita posloupnosti'), [{'words': ['posloupnosti', 'bodě', 'derivace'], 'rank': 0.492}, {'words': ['výraz', 'limita', 'derivace'], 'rank': 0.492}, {'words': ['posloupnosti', 'výraz', 'derivace'], 'rank': 0.492}, {'words': ['bodě', 'limita', 'derivace'], 'rank': 0.492}, {'words': ['obor', 'množiny', 'definiční', 'posloupnosti', 'derivace'], 'rank': 0.393}, {'words': ['posloupnosti', 'argument', 'derivace'], 'rank': 0.367}])
		ass(fun('Procenta OR scitani'), [{'words': ['Procenta', 'zlomku', 'výraz'], 'rank': 0.679}, {'words': ['zlomku', 'scitani', 'výraz'], 'rank': 0.625}, {'words': ['zlomek', 'zlomku', 'scitani'], 'rank': 0.583}, {'words': ['zlomku', 'scitani', 'reálná'], 'rank': 0.429}, {'words': ['Procenta', 'zlomku', 'reálná'], 'rank': 0.429}, {'words': ['Procenta', 'zlomku', 'racionální'], 'rank': 0.393}])


	def execute(self, dtb, q):
		return self.runShell(dtb, q).decode("utf-8")

	def runShell(self, dtb, q):
		cmd = PYTHON3 + ROOT_FOLDER + 'src/search '
		with Popen(cmd + '-d ' + dtb + ' -q "' + q + '" -f json -t', stdout=PIPE, shell=True) as sh:
			return sh.stdout.read()
		
		


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()