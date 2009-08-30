import unittest

import os

from extractor import *

class CrosswordDotInfoXmlExtractorTest(unittest.TestCase):
	def setUp(self):
		self.xml = open(os.path.join(os.path.dirname(__file__),'12110.xml.17'), 'r').read()
		self.cryptic_xml = open(os.path.join(os.path.dirname(__file__),'24656.xml.16'), 'r').read()
		self.extractor = CrosswordDotInfoXmlExtractor()

	def test_should_extract_title_based_on_type_and_identifier(self):
		self.extractor.parse(self.xml)
		self.assertEqual(self.extractor.title(), 'Quick Crossword No. 12110')

	def test_should_get_type_from_title(self):
		self.extractor.parse(self.xml)
		self.assertEqual(self.extractor.type(), 'quick')

	def test_should_extract_creator(self):
		self.extractor.parse(self.xml)
		self.assertEqual(self.extractor.creator(), 'Fiore')

	def test_should_extract_identifier(self):
		self.extractor.parse(self.xml)
		self.assertEqual(self.extractor.identifier(), 12110)

	def test_should_extract_width(self):
		self.extractor.parse(self.xml)
		self.assertEqual(self.extractor.width(), 13)

	def test_should_extract_height(self):
		self.extractor.parse(self.xml)
		self.assertEqual(self.extractor.height(), 13)

	def test_all_squares_should_be_in_letters_dictionary(self):
		self.extractor.parse(self.xml)
		letters = self.extractor.letters()
		self.assertEqual(len(letters), 13 * 13)

	def test_squares_with_a_letter_should_have_letter_in_dictionary(self):
		self.extractor.parse(self.xml)
		letters = self.extractor.letters()
		self.assertEqual(letters[1,1], 'D')

	def test_squares_with_no_letter_should_be_empty_string_in_dictionary(self):
		self.extractor.parse(self.xml)
		letters = self.extractor.letters()
		self.assertEqual(letters[1,9], '')

	def test_clues_should_be_in_directional_dictionaries_including_length(self):
		self.extractor.parse(self.xml)
		across = self.extractor.across_clues()
		self.assertEqual(across['1'], 'Be bold enough (4)')
		down = self.extractor.down_clues()
		self.assertEqual(down['1'], 'Type of compass used for measuring distance (8)')

	def test_should_be_able_to_extract_see_other_type_clue(self):
		self.extractor.parse(self.cryptic_xml)
		down = self.extractor.down_clues()
		self.assertEqual(down['19'], 'See 4')

	def test_should_extract_clue_where_answer_spans_multiple_numbers(self):
		self.extractor.parse(self.cryptic_xml)
		down = self.extractor.down_clues()
		self.assertEqual(down['4'], 'Fearful hen I can, oddly, put in kind of curry (7,7)')
		
	def test_should_provide_entry_to_clue_array_even_if_only_in_joint_clue(self):
		self.extractor.parse(self.cryptic_xml)
		across = self.extractor.across_clues()
		self.assertTrue('17' in across)
		self.assertEqual(across['17'], 'See 15')

	def test_should_not_put_24_in_across_dictionary(self):
		self.extractor.parse(self.cryptic_xml)
		across = self.extractor.across_clues()
		self.assertFalse('24down' in across)

class GuCrosswordXmlExtractorTest(unittest.TestCase):
	def setUp(self):
		self.xml = open(os.path.join(os.path.dirname(__file__),'1,,25032009,00.xml'), 'r').read()
		self.extractor = GuCrosswordXmlExtractor()

	def test_should_extract_title_based_on_xml(self):
		self.extractor.parse(self.xml)
		self.assertEqual(self.extractor.title(), 'Cryptic Crossword No. 24656')

if __name__ == '__main__':
	unittest.main()
