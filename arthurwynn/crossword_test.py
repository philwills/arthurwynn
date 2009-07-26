import unittest

from crossword import Crossword

class CrosswordTest(unittest.TestCase):
	def test_should_provide_access_to_across_words(self):
		crossword = StockCrossword()
		one_across = crossword.across_words()[0]
		self.assertEqual(one_across.number, 1)
		self.assertEqual(one_across.clue, 'Really not very clean')
		self.assertEqual(one_across.solution, 'FILTHY')
				
	def test_should_provide_access_to_down_words(self):
		crossword = StockCrossword()
		one_down = crossword.down_words()[0]
		self.assertEqual(one_down.number, 1)
		self.assertEqual(one_down.clue, 'Unsophisticated')
		self.assertEqual(one_down.solution, 'FOLKSY')

	def test_should_list_intersections(self):
		crossword = StockCrossword()
		intersections = crossword.intersections()
		self.assertEqual(intersections['1-across-1'], '1-down-1')

	def test_can_build_solution_from_letters_dictionary(self):
		crossword = Crossword()
		crossword.size(3)
		letters = {}
		letters[1,1] = 'A'
		letters[2,1] = 'B'
		letters[3,1] = ''
		letters[1,2] = ''
		letters[2,2] = 'C'
		letters[3,2] = 'D'
		letters[1,3] = 'E'
		letters[2,3] = 'F'
		letters[3,3] = 'G'
		crossword.build_solution(letters)
		self.assertEquals(crossword.across_solutions[0], 'AB')
		self.assertEquals(crossword.across_solutions[2], 'EFG')
		self.assertEquals(crossword.down_solutions[0], 'BCF')

	def test_should_provide_link_to_full_version(self):
		crossword = Crossword()
		crossword.type = 'quick'
		crossword.number = 42
		self.assertEqual(crossword.url(), '/microapp/resources/quick/42')

	def test_should_provide_helpful_title_with_creator(self):
		crossword = Crossword()
		crossword.type = 'cryptic'
		crossword.number = 42
		crossword.creator = 'Philus Willus'
		self.assertEqual(crossword.title(), 'Cryptic Crossword No. 42 set by Philus Willus')
		
	def test_should_provide_helpful_title_when_no_creator_set(self):
		crossword = Crossword()
		crossword.type = 'cryptic'
		crossword.number = 42
		self.assertEqual(crossword.title(), 'Cryptic Crossword No. 42')

	def test_should_just_use_name_for_title_if_no_type(self):
		crossword = Crossword()
		crossword.name = 'Geoffrey'
		self.assertEqual(crossword.title(), 'Geoffrey')

	def test_should_provide_blanks(self):
		crossword = StockCrossword()
		
		self.assertEqual(crossword.blanks()[1], [7])
		
				
class StockCrossword(Crossword):
	def __init__(self):
		self.name = "Stock Crossword"
		self.num_grid_rows = 13
		self.num_grid_cols = 13
		self.across_nums = [1, 4, 8, 9, 10, 11, 12, 17, 19, 21, 22, 23,24,]
		self.across_clues = ["Really not very clean", "SWITCH", "LIBEL", "HUSBAND", "SURGEON", "FRAIL", "AMARYLLIS", "DUMPY", "OBLOQUY", "GIMMICK", "MAORI", "OYSTER", "STEADY",]
		self.across_solutions = ["FILTHY", "SWITCH", "LIBEL", "HUSBAND", "SURGEON", "FRAIL", "AMARYLLIS", "DUMPY", "OBLOQUY", "GIMMICK", "MAORI", "OYSTER", "STEADY",]
		self.across_x = [1, 8, 1, 7, 1, 9, 3, 1, 7, 1, 9, 1, 8,]
		self.across_y = [1, 1, 3, 3, 5, 5, 7, 9, 9, 11, 11, 13, 13,]
		self.down_nums = [1, 2, 3, 5, 6, 7, 9, 13, 14, 15, 16, 18, 20,]
		self.down_clues = ["Unsophisticated", "LIBERIA", "HALVE", "WISTFUL", "TRALA", "HUDDLE", "HONKYTONK", "ANYTIME", "SEQUOIA", "ADAGIO", "TYPIFY", "MUMPS", "LIMIT",]
		self.down_solutions = ["FOLKSY", "LIBERIA", "HALVE", "WISTFUL", "TRALA", "HUDDLE", "HONKYTONK", "ANYTIME", "SEQUOIA", "ADAGIO", "TYPIFY", "MUMPS", "LIMIT",]
		self.down_x = [1, 3, 5, 9, 11, 13, 7, 5, 11, 1, 13, 3, 9,]
		self.down_y = [1, 1, 1, 1, 1, 1, 3, 7, 7, 8, 8, 9, 9,]

if __name__ == '__main__':
	unittest.main()
