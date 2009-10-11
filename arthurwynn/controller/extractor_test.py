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
		self.assertEqual(letters[0,0], 'D')

	def test_squares_with_no_letter_should_be_empty_string_in_dictionary(self):
		self.extractor.parse(self.xml)
		letters = self.extractor.letters()
		self.assertEqual(letters[0,8], '')

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

	def test_should_get_type_from_title(self):
		self.extractor.parse(self.xml)
		self.assertEqual(self.extractor.type(), 'Cryptic')

	def test_should_extract_creator(self):
		self.extractor.parse(self.xml)
		self.assertEqual(self.extractor.creator(), 'Brendan')

	def test_should_extract_identifier(self):
		self.extractor.parse(self.xml)
		self.assertEqual(self.extractor.identifier(), 24656)

	def test_should_extract_width(self):
		self.extractor.parse(self.xml)
		self.assertEqual(self.extractor.width(), 15)

	def test_should_extract_height(self):
		self.extractor.parse(self.xml)
		self.assertEqual(self.extractor.height(), 15)

	def test_all_across_numbers_extracted(self):
		self.extractor.parse(self.xml)
		across_nums = self.extractor.across_nums()
		self.assertEqual(across_nums, [8,9,10,11,12,14,15,17,20,22,23,24,25,26])

	def test_all_down_numbers_extracted(self):
		self.extractor.parse(self.xml)
		down_nums = self.extractor.down_nums()
		self.assertEqual(down_nums, [1,2,3,4,5,6,7,13,16,18,19,21,22,24])

	def test_coordinates_extracted(self):
		self.extractor.parse(self.xml)
		self.assertEqual(self.extractor.across_x(), [0,9,0,5,0,7,0,8,0,9,0,11,0,7])
		self.assertEqual(self.extractor.down_y(), [0,0,0,0,0,0,0,5,7,7,8,9,9,11])

	def test_clue_extracted(self):
		self.extractor.parse(self.xml)
		self.assertEqual(self.extractor.across_clues()[0], 'Players collectively demolish extra food(4,4)')

	def test_solution_extracted(self):
		self.extractor.parse(self.xml)
		self.assertEqual(self.extractor.across_solutions()[0], 'SIDEDISH')

if __name__ == '__main__':
	unittest.main()
