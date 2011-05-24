import unittest
from common.string import *
import string


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
		self.assertEquals('helloworld', remove_nonletters('hello__world!!! :-)) <3 :-|'))
		self.assertEquals('hello  world   ', remove_nonletters('hello__world!?!', ' '))
		
	def test_normalize_text(self):
		self.assertEquals('háčky čárky to je věda dva tři', 
						normalize_text('Háčky čárky, to je věda! Dva + Tři = __?'))
		
	def test_replace_white_spaces(self):
		self.assertEqual('ssdasasasdasdaasdasd', 
						replace_white_spaces('   ssd as as as d    asd a as dasd  '))
		self.assertEqual('text with white spaces', 
						replace_white_spaces('text with  white  		 spaces', ' '))
		
	def test_replace_single(self):
		self.assertEquals('??efghijklmnopqrstuvwxyz', 
						replace_single(string.ascii_lowercase, ['a', 'bcd', 'xx'], '?'))
		
	def test_replace_dict(self):
		self.assertEquals('?bcdefghijklmnopqrstuvwend', 
						replace_dict(string.ascii_lowercase, {'a':'?', 'xyz':'end'}))