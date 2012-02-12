import unittest
import string
from common.list import splitlist
from common.string import sjoin, isletter, strip_accents, remove_nonletters,\
	normalize_text, replace_white_spaces, replace_single, replace_dict

class TestString(unittest.TestCase):
	def test_sjoin(self):
		self.assertEqual('', sjoin([]))
		self.assertEqual('123', sjoin([1,2,3]))
		self.assertEqual('12[3, 4]', sjoin([1,2,[3,4]]))
		
	def test_isletter(self):
		map(lambda x: self.assert_(isletter(x)), 'dgpnéíáýžřčšěÉÍÁÝŽŘČŠČŠŮÚůú'.split())
		map(lambda x: self.assert_(not(isletter(x))), string.punctuation + string.digits)
		
	def test_strip_accents(self):
		self.assertEqual('escrzyaieuuESCRZYAIEUU', strip_accents('ěščřžýáíéúůĚŠČŘŽÝÁÍÉÚŮ'))
		
	def test_remove_nonletters(self):
		self.assertEqual('helloworld', remove_nonletters('hello__world!!! :-)) <3 :-|'))
		self.assertEqual('hello  world   ', remove_nonletters('hello__world!?!', ' '))
		
	def test_normalize_text(self):
		self.assertEqual('háčky čárky to je věda dva tři', 
						normalize_text('Háčky čárky, to je věda! Dva + Tři = __?'))
		
	def test_replace_white_spaces(self):
		self.assertEqual('ssdasasasdasdaasdasd', 
						replace_white_spaces('   ssd as as as d    asd a as dasd  '))
		self.assertEqual('text with white spaces', 
						replace_white_spaces('text with  white  		 spaces', ' '))
		
	def test_replace_single(self):
		self.assertEqual('??efghijklmnopqrstuvwxyz', 
						replace_single(string.ascii_lowercase, ['a', 'bcd', 'xx'], '?'))
		
	def test_replace_dict(self):
		self.assertEqual('?bcdefghijklmnopqrstuvwend', 
						replace_dict(string.ascii_lowercase, {'a':'?', 'xyz':'end'}))
		

class TestList(unittest.TestCase):
	def test_splitlist(self):
		self.assertEqual([[1, 2, 3], [4, 5, 6], [7, 8, 9]], splitlist([1,2,3,'x',4,5,6,'x',7,8,9], 'x'))
		self.assertEqual([[1, 2, 3, 'x', 4, 5, 6, 'x', 7, 8, 9]], splitlist([1,2,3,'x',4,5,6,'x',7,8,9], 'xy'))
		self.assertEqual([[], [], []], splitlist(['a','a'], 'a'))
		
if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()