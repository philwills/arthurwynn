import unittest

import os

from GuCrosswordXmlExtractor import GuCrosswordXmlExtractor


class GuCrosswordXmlExtractorTest(unittest.TestCase):
    def setUp(self):
        self.xml = open(
            os.path.join(os.path.dirname(__file__), "1,,25032009,00.xml"), "r"
        ).read()
        self.extractor = GuCrosswordXmlExtractor()

    def test_should_extract_title_based_on_xml(self):
        self.extractor.parse(self.xml)
        self.assertEqual(self.extractor.title(), "Cryptic Crossword No. 24656")

    def test_should_get_type_from_title(self):
        self.extractor.parse(self.xml)
        self.assertEqual(self.extractor.type(), "Cryptic")

    def test_should_extract_creator(self):
        self.extractor.parse(self.xml)
        self.assertEqual(self.extractor.creator(), "Brendan")

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
        self.assertEqual(
            across_nums, [8, 9, 10, 11, 12, 14, 15, 17, 20, 22, 23, 24, 25, 26]
        )

    def test_all_down_numbers_extracted(self):
        self.extractor.parse(self.xml)
        down_nums = self.extractor.down_nums()
        self.assertEqual(down_nums, [1, 2, 3, 4, 5, 6, 7, 13, 16, 18, 19, 21, 22, 24])

    def test_coordinates_extracted(self):
        self.extractor.parse(self.xml)
        self.assertEqual(
            self.extractor.across_x(), [0, 9, 0, 5, 0, 7, 0, 8, 0, 9, 0, 11, 0, 7]
        )
        self.assertEqual(
            self.extractor.down_y(), [0, 0, 0, 0, 0, 0, 0, 5, 7, 7, 8, 9, 9, 11]
        )

    def test_clue_extracted(self):
        self.extractor.parse(self.xml)
        self.assertEqual(
            self.extractor.across_clues()[0],
            "Players collectively demolish extra food(4,4)",
        )

    def test_solution_extracted(self):
        self.extractor.parse(self.xml)
        self.assertEqual(self.extractor.across_solutions()[0], "SIDEDISH")


if __name__ == "__main__":
    unittest.main()
