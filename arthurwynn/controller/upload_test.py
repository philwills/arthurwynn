import unittest

from mockito import *

from upload import CrosswordUploadPage

from arthurwynn.crossword import Crossword

class CrosswordUploadPageTest(unittest.TestCase):
	def setUp(self):
		self.upload_page = CrosswordUploadPage()

		self.crossword_repository = Mock()
		self.upload_page.repository = self.crossword_repository

		extractor = Mock()
		when(extractor).width().thenReturn(0)
		when(extractor).type().thenReturn("quick")
		when(extractor).identifier().thenReturn(42)
		self.upload_page.extractor = extractor

		request = Mock()
		when(request).get('xml').thenReturn("")
		self.upload_page.request = request	
		self.upload_page.response = None	

	def test_should_create_new_crossword_if_no_existing(self):
		when(self.crossword_repository).find("quick", 42).thenReturn(None)
		new_xword = Crossword()
		when(self.crossword_repository).create().thenReturn(new_xword)
		
		self.upload_page.post()

		verify(self.crossword_repository).add_or_update(new_xword)
		
	def test_should_update_existing_crossword_if_number_and_type_the_same(self):
		old_xword = Crossword()
		when(self.crossword_repository).find("quick", 42).thenReturn(old_xword)

		self.upload_page.post()

		verify(self.crossword_repository).add_or_update(old_xword)

from upload import CrosswordDotInfoXmlExtractor

class CrosswordDotInfoXmlExtractorTest(unittest.TestCase):
	def setUp(self):
		self.xml = u"""<?xml version="1.0" encoding="UTF-8"?>
<crossword-compiler xmlns="http://crossword.info/xml/crossword-compiler">
<rectangular-puzzle xmlns="http://crossword.info/xml/rectangular-puzzle" alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ">
<metadata>
<title>gdn.quick</title>
<creator>Fiore</creator>
<copyright></copyright>
<description></description>
<identifier>12110</identifier>
<status>Desk</status>
</metadata>
<crossword>
<grid width="13" height="13">
<grid-look numbering-scheme="normal" clue-square-divider-width="0.7"></grid-look>
<cell x="1" y="1" solution="D" number="1"></cell>
<cell x="1" y="2" solution="I"></cell>
<cell x="1" y="3" solution="V" number="9"></cell>
<cell x="1" y="4" solution="I"></cell>
<cell x="1" y="5" solution="D" number="11"></cell>
<cell x="1" y="6" solution="E"></cell>
<cell x="1" y="7" solution="R" number="14"></cell>
<cell x="1" y="8" solution="S"></cell>
<cell x="1" y="9" type="block"></cell>
<cell x="1" y="10" solution="W" number="21"></cell><cell x="1" y="11" solution="A" number="22"></cell><cell x="1" y="12" solution="I"></cell><cell x="1" y="13" solution="F" number="24"></cell><cell x="2" y="1" solution="A"></cell><cell x="2" y="2" type="block"></cell><cell x="2" y="3" solution="I"></cell><cell x="2" y="4" type="block"></cell><cell x="2" y="5" solution="O"></cell><cell x="2" y="6" type="block"></cell><cell x="2" y="7" solution="E"></cell><cell x="2" y="8" type="block"></cell><cell x="2" y="9" solution="B" number="17"></cell><cell x="2" y="10" type="block"></cell><cell x="2" y="11" solution="L"></cell><cell x="2" y="12" type="block"></cell><cell x="2" y="13" solution="I"></cell><cell x="3" y="1" solution="R" number="2"></cell><cell x="3" y="2" solution="O"></cell><cell x="3" y="3" solution="C"></cell><cell x="3" y="4" solution="K"></cell><cell x="3" y="5" solution="Y"></cell><cell x="3" y="6" type="block"></cell><cell x="3" y="7" solution="M" number="15"></cell><cell x="3" y="8" solution="E"></cell><cell x="3" y="9" solution="A"></cell><cell x="3" y="10" solution="N"></cell><cell x="3" y="11" solution="D"></cell><cell x="3" y="12" solution="E"></cell><cell x="3" y="13" solution="R"></cell><cell x="4" y="1" solution="E"></cell><cell x="4" y="2" type="block"></cell><cell x="4" y="3" solution="I"></cell><cell x="4" y="4" type="block"></cell><cell x="4" y="5" solution="E"></cell><cell x="4" y="6" type="block"></cell><cell x="4" y="7" solution="O"></cell><cell x="4" y="8" type="block"></cell><cell x="4" y="9" solution="Z"></cell><cell x="4" y="10" type="block"></cell><cell x="4" y="11" solution="E"></cell><cell x="4" y="12" type="block"></cell><cell x="4" y="13" solution="E"></cell><cell x="5" y="1" type="block"></cell><cell x="5" y="2" solution="H" number="8"></cell><cell x="5" y="3" solution="O"></cell><cell x="5" y="4" solution="R"></cell><cell x="5" y="5" solution="N"></cell><cell x="5" y="6" solution="E"></cell><cell x="5" y="7" solution="T"></cell><cell x="5" y="8" type="block"></cell><cell x="5" y="9" solution="A" number="18"></cell><cell x="5" y="10" solution="R"></cell><cell x="5" y="11" solution="R"></cell><cell x="5" y="12" solution="O"></cell><cell x="5" y="13" solution="W"></cell><cell x="6" y="1" solution="A" number="3"></cell><cell x="6" y="2" type="block"></cell><cell x="6" y="3" solution="U"></cell><cell x="6" y="4" type="block"></cell><cell x="6" y="5" type="block"></cell><cell x="6" y="6" type="block"></cell><cell x="6" y="7" solution="E"></cell><cell x="6" y="8" type="block"></cell><cell x="6" y="9" solution="A"></cell><cell x="6" y="10" type="block"></cell><cell x="6" y="11" type="block"></cell><cell x="6" y="12" type="block"></cell><cell x="6" y="13" solution="O"></cell><cell x="7" y="1" solution="D" number="4"></cell><cell x="7" y="2" solution="I"></cell><cell x="7" y="3" solution="S"></cell><cell x="7" y="4" solution="P"></cell><cell x="7" y="5" solution="A" number="12"></cell><cell x="7" y="6" solution="T"></cell><cell x="7" y="7" solution="C"></cell><cell x="7" y="8" solution="H"></cell><cell x="7" y="9" solution="R"></cell><cell x="7" y="10" solution="I"></cell><cell x="7" y="11" solution="D" number="23"></cell><cell x="7" y="12" solution="E"></cell><cell x="7" y="13" solution="R"></cell><cell x="8" y="1" solution="V"></cell><cell x="8" y="2" type="block"></cell><cell x="8" y="3" type="block"></cell><cell x="8" y="4" type="block"></cell><cell x="8" y="5" solution="R"></cell><cell x="8" y="6" type="block"></cell><cell x="8" y="7" solution="O"></cell><cell x="8" y="8" type="block"></cell><cell x="8" y="9" type="block"></cell><cell x="8" y="10" type="block"></cell><cell x="8" y="11" solution="O"></cell><cell x="8" y="12" type="block"></cell><cell x="8" y="13" solution="K"></cell><cell x="9" y="1" solution="A" number="5"></cell><cell x="9" y="2" solution="S"></cell><cell x="9" y="3" solution="C" number="10"></cell><cell x="9" y="4" solution="O"></cell><cell x="9" y="5" solution="T"></cell><cell x="9" y="6" type="block"></cell><cell x="9" y="7" solution="N" number="16"></cell><cell x="9" y="8" solution="O"></cell><cell x="9" y="9" solution="B" number="19"></cell><cell x="9" y="10" solution="A"></cell><cell x="9" y="11" solution="L"></cell><cell x="9" y="12" solution="L"></cell><cell x="9" y="13" type="block"></cell><cell x="10" y="1" solution="N"></cell><cell x="10" y="2" type="block"></cell><cell x="10" y="3" solution="O"></cell><cell x="10" y="4" type="block"></cell><cell x="10" y="5" solution="I"></cell><cell x="10" y="6" type="block"></cell><cell x="10" y="7" solution="T"></cell><cell x="10" y="8" type="block"></cell><cell x="10" y="9" solution="E"></cell><cell x="10" y="10" type="block"></cell><cell x="10" y="11" solution="E"></cell><cell x="10" y="12" type="block"></cell><cell x="10" y="13" solution="R" number="25"></cell><cell x="11" y="1" solution="C" number="6"></cell><cell x="11" y="2" solution="R"></cell><cell x="11" y="3" solution="U"></cell><cell x="11" y="4" solution="I"></cell><cell x="11" y="5" solution="S"></cell><cell x="11" y="6" solution="E"></cell><cell x="11" y="7" solution="R"></cell><cell x="11" y="8" type="block"></cell><cell x="11" y="9" solution="F" number="20"></cell><cell x="11" y="10" solution="I"></cell><cell x="11" y="11" solution="F"></cell><cell x="11" y="12" solution="T"></cell><cell x="11" y="13" solution="H"></cell><cell x="12" y="1" solution="E"></cell><cell x="12" y="2" type="block"></cell><cell x="12" y="3" solution="N"></cell><cell x="12" y="4" type="block"></cell><cell x="12" y="5" solution="T"></cell><cell x="12" y="6" type="block"></cell><cell x="12" y="7" solution="O"></cell><cell x="12" y="8" type="block"></cell><cell x="12" y="9" solution="I"></cell><cell x="12" y="10" type="block"></cell><cell x="12" y="11" solution="U"></cell><cell x="12" y="12" type="block"></cell><cell x="12" y="13" solution="E"></cell><cell x="13" y="1" solution="D" number="7"></cell><cell x="13" y="2" solution="A"></cell><cell x="13" y="3" solution="T"></cell><cell x="13" y="4" solution="A"></cell><cell x="13" y="5" type="block"></cell><cell x="13" y="6" solution="F" number="13"></cell><cell x="13" y="7" solution="L"></cell><cell x="13" y="8" solution="O"></cell><cell x="13" y="9" solution="T"></cell><cell x="13" y="10" solution="I"></cell><cell x="13" y="11" solution="L"></cell><cell x="13" y="12" solution="L"></cell><cell x="13" y="13" solution="A"></cell></grid><word id="1" x="1-4" y="1"></word><word id="2" x="6-13" y="1"></word><word id="3" x="1-7" y="3"></word><word id="4" x="9-13" y="3"></word><word id="5" x="1-5" y="5"></word><word id="6" x="7-12" y="5"></word><word id="7" x="1-13" y="7" solution="remote control"></word><word id="8" x="2-7" y="9"></word><word id="9" x="9-13" y="9"></word><word id="10" x="1-5" y="11"></word><word id="11" x="7-13" y="11"></word><word id="12" x="1-8" y="13"></word><word id="13" x="10-13" y="13"></word><word id="14" x="1" y="1-8"></word><word id="15" x="3" y="1-5"></word><word id="16" x="7" y="1-13" solution="dispatch rider"></word><word id="17" x="9" y="1-5"></word><word id="18" x="11" y="1-7"></word><word id="19" x="13" y="1-4"></word><word id="20" x="5" y="2-7"></word><word id="21" x="13" y="6-13"></word><word id="22" x="3" y="7-13"></word><word id="23" x="9" y="7-12" solution="no ball"></word><word id="24" x="5" y="9-13"></word><word id="25" x="11" y="9-13"></word><word id="26" x="1" y="10-13"></word>
<clues ordering="normal"><title><b>Across</b></title><clue word="1" number="1" format="4">Be bold enough</clue>
</clues>
<clues ordering="normal"><title><b>Down</b></title><clue word="14" number="1" format="8">Type of compass used for measuring distance</clue>
</clues></crossword></rectangular-puzzle>
</crossword-compiler>
"""
		self.extractor = CrosswordDotInfoXmlExtractor()
		self.extractor.parse(self.xml)

	def test_should_extract_title_from_xml(self):
		self.assertEqual(self.extractor.title(), 'gdn.quick')

	def test_should_get_type_from_title(self):
		self.assertEqual(self.extractor.type(), 'quick')

	def test_should_extract_creator(self):
		self.assertEqual(self.extractor.creator(), 'Fiore')

	def test_should_extract_identifier(self):
		self.assertEqual(self.extractor.identifier(), 12110)

	def test_should_extract_width(self):
		self.assertEqual(self.extractor.width(), 13)

	def test_should_extract_height(self):
		self.assertEqual(self.extractor.height(), 13)

	def test_all_squares_should_be_in_letters_dictionary(self):
		letters = self.extractor.letters()
		self.assertEqual(len(letters), 13 * 13)

	def test_squares_with_a_letter_should_have_letter_in_dictionary(self):
		letters = self.extractor.letters()
		self.assertEqual(letters[1,1], 'D')

	def test_squares_with_no_letter_should_be_empty_string_in_dictionary(self):
		letters = self.extractor.letters()
		self.assertEqual(letters[1,9], '')

	def test_clues_should_be_in_directional_dictionaries_including_length(self):
		across = self.extractor.across_clues()
		self.assertEqual(across['1'], 'Be bold enough (4)')
		down = self.extractor.down_clues()
		self.assertEqual(down['1'], 'Type of compass used for measuring distance (8)')

if __name__ == '__main__':
	unittest.main()
