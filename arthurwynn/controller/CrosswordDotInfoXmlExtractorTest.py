import unittest

import os

from CrosswordDotInfoXmlExtractor import CrosswordDotInfoXmlExtractor, Coordinate


class CrosswordDotInfoXmlExtractorTest(unittest.TestCase):
    def setUp(self):
        self.xml = open(
            os.path.join(os.path.dirname(__file__), "12110.xml.17"), "r"
        ).read()
        self.cryptic_xml = open(
            os.path.join(os.path.dirname(__file__), "24656.xml.16"), "r"
        ).read()
        self.extractor = CrosswordDotInfoXmlExtractor()

    def test_should_extract_title_based_on_type_and_identifier(self):
        crossword = self.extractor.parse(self.xml)
        self.assertEqual(crossword.title, "Quick Crossword No. 12110")

    def test_should_get_type_from_title(self):
        crossword = self.extractor.parse(self.xml)
        self.assertEqual(crossword.type._value_, "quick")

    def test_should_extract_creator(self):
        crossword = self.extractor.parse(self.xml)
        self.assertEqual(crossword.creator, "Fiore")

    def test_should_extract_identifier(self):
        crossword = self.extractor.parse(self.xml)
        self.assertEqual(crossword.identifier, 12110)

    def test_should_extract_width(self):
        crossword = self.extractor.parse(self.xml)
        self.assertEqual(crossword.width, 13)

    def test_should_extract_height(self):
        crossword = self.extractor.parse(self.xml)
        self.assertEqual(crossword.height, 13)

    def test_all_squares_should_be_in_letters_dictionary(self):
        crossword = self.extractor.parse(self.xml)
        letters = crossword.letters
        self.assertEqual(len(letters), 13 * 13)

    def test_squares_with_a_letter_should_have_letter_in_dictionary(self):
        crossword = self.extractor.parse(self.xml)
        letters = crossword.letters()
        self.assertEqual(letters[Coordinate(0, 0)], "D")

    def test_squares_with_no_letter_should_be_empty_string_in_dictionary(self):
        crossword = self.extractor.parse(self.xml)
        letters = crossword.letters()
        self.assertEqual(letters[Coordinate(0, 8)], "")

    def test_clues_should_be_in_directional_dictionaries_including_length(self):
        crossword = self.extractor.parse(self.xml)
        across = crossword.across_clues()
        self.assertEqual(across["1"], "Be bold enough (4)")
        down = crossword.down_clues()
        self.assertEqual(down["1"], "Type of compass used for measuring distance (8)")

    def test_should_be_able_to_extract_see_other_type_clue(self):
        crossword = self.extractor.parse(self.cryptic_xml)
        down = crossword.down_clues()
        self.assertEqual(down["19"], "See 4")

    def test_should_extract_clue_where_answer_spans_multiple_numbers(self):
        crossword = self.extractor.parse(self.cryptic_xml)
        down = crossword.down_clues()
        self.assertEqual(
            down["4"], "Fearful hen I can, oddly, put in kind of curry (7,7)"
        )

    def test_should_provide_entry_to_clue_array_even_if_only_in_joint_clue(self):
        crossword = self.extractor.parse(self.cryptic_xml)
        across = crossword.across_clues()
        self.assertTrue("17" in across)
        self.assertEqual(across["17"], "See 15")

    def test_should_not_put_24_in_across_dictionary(self):
        crossword = self.extractor.parse(self.cryptic_xml)
        across = crossword.across_clues()
        self.assertFalse("24down" in across)

if __name__ == "__main__":
    unittest.main()
