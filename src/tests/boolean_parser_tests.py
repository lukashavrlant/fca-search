import unittest
from retrieval.boolean_parser import BooleanParser


class BooleanParserTest(unittest.TestCase):
	parser = BooleanParser()
	
	def test_pure_parse(self):
		fun = lambda x: repr(self.parser._pure_parse(x))
		ass = self.assertEqual
		
		ass(fun('arg1 AND arg2 OR arg3'), "(('arg1' AND 'arg2') OR 'arg3')")
		ass(fun('(ARG AND ARG (ARG OR NOT ARG))'), "('ARG' AND 'ARG' AND ('ARG' OR (NOT('ARG'))))")
		ass(fun(''), '()')
		ass(fun('OR OR (AND test NOT)'), "(() OR () OR ('test' AND ''))")
	
	def test_parse(self):
		fun = lambda x: repr(self.parser.parse(x))
		ass = self.assertEqual
		
		ass(fun('OR OR (AND test NOT)'), "'test'")
		ass(fun('((star AND wars) AND NOT trek) OR ((star AND trek) OR TOS)'), "((('star' AND 'wars') AND NOT('trek')) OR (('star' AND 'trek') OR 'TOS'))")
		ass(fun(''), "''")