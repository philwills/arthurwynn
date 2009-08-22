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

		self.request = Mock()
		when(self.request).get('xml').thenReturn("")
		self.upload_page.request = self.request	
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

	def test_should_set_xml_on_crossword(self):
		old_xword = Crossword()
		when(self.crossword_repository).find("quick", 42).thenReturn(old_xword)
		xml = "<xml>honest</xml>"
		when(self.request).get('xml').thenReturn(xml)

		self.upload_page.post()

		self.assertEqual(xml, old_xword.xml)

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
		self.cryptic_xml = u"""<?xml version="1.0" encoding="UTF-8"?>
<crossword-compiler xmlns="http://crossword.info/xml/crossword-compiler">
<rectangular-puzzle xmlns="http://crossword.info/xml/rectangular-puzzle" alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ">
<metadata><title>gdn.cryptic</title><creator>Paul</creator><copyright></copyright><description></description><identifier>24623</identifier><status>Wtiter</status></metadata>
<crossword><grid width="15" height="15"><grid-look numbering-scheme="normal" clue-square-divider-width="0.7"></grid-look>
<cell x="1" y="1" type="block"></cell>
<cell x="1" y="2" solution="S" number="8"></cell>
<cell x="1" y="3" type="block"></cell>
<cell x="1" y="4" solution="L" number="10"></cell>
<cell x="1" y="5" type="block"></cell>
<cell x="1" y="6" solution="M" number="12"></cell>
<cell x="1" y="7" type="block"></cell>
<cell x="1" y="8" solution="N" number="15"></cell>
<cell x="1" y="9" type="block"></cell>
<cell x="1" y="10" solution="D" number="20"></cell>
<cell x="1" y="11" type="block"></cell>
<cell x="1" y="12" solution="F" number="23"></cell>
<cell x="1" y="13" type="block"></cell>
<cell x="1" y="14" solution="T" number="25"></cell>
<cell x="1" y="15" type="block"></cell>
<cell x="2" y="1" solution="R" number="1"></cell>
<cell x="2" y="2" solution="I"></cell>
<cell x="2" y="3" solution="T"></cell>
<cell x="2" y="4" solution="E"></cell>
<cell x="2" y="5" solution="N"></cell>
<cell x="2" y="6" solution="U"></cell>
<cell x="2" y="7" solution="T"></cell>
<cell x="2" y="8" solution="O"></cell>
<cell x="2" y="9" type="block"></cell>
<cell x="2" y="10" solution="E" number="21"></cell>
<cell x="2" y="11" solution="A"></cell>
<cell x="2" y="12" solution="R"></cell>
<cell x="2" y="13" solution="T"></cell>
<cell x="2" y="14" solution="H"></cell>
<cell x="2" y="15" solution="Y"></cell>
<cell x="3" y="1" type="block"></cell>
<cell x="3" y="2" solution="D"></cell>
<cell x="3" y="3" type="block"></cell>
<cell x="3" y="4" solution="O"></cell>
<cell x="3" y="5" type="block"></cell>
<cell x="3" y="6" solution="M"></cell>
<cell x="3" y="7" type="block"></cell>
<cell x="3" y="8" solution="M"></cell>
<cell x="3" y="9" type="block"></cell>
<cell x="3" y="10" solution="V"></cell>
<cell x="3" y="11" type="block"></cell>
<cell x="3" y="12" solution="I"></cell>
<cell x="3" y="13" type="block"></cell>
<cell x="3" y="14" solution="E"></cell>
<cell x="3" y="15" type="block"></cell>
<cell x="4" y="1" solution="J" number="2"></cell>
<cell x="4" y="2" solution="E"></cell>
<cell x="4" y="3" solution="A"></cell>
<cell x="4" y="4" solution="N"></cell>
<cell x="4" y="5" type="block"></cell>
<cell x="4" y="6" solution="B" number="13"></cell>
<cell x="4" y="7" solution="E"></cell>
<cell x="4" y="8" solution="I"></cell>
<cell x="4" y="9" solution="J"></cell>
<cell x="4" y="10" solution="I"></cell>
<cell x="4" y="11" solution="N"></cell>
<cell x="4" y="12" solution="G"></cell>
<cell x="4" y="13" solution="E"></cell>
<cell x="4" y="14" solution="S"></cell>
<cell x="4" y="15" solution="E"></cell>
<cell x="5" y="1" type="block"></cell>
<cell x="5" y="2" solution="D"></cell>
<cell x="5" y="3" type="block"></cell>
<cell x="5" y="4" type="block"></cell>
<cell x="5" y="5" type="block"></cell>
<cell x="5" y="6" solution="A"></cell>
<cell x="5" y="7" type="block"></cell>
<cell x="5" y="8" solution="N"></cell>
<cell x="5" y="9" type="block"></cell>
<cell x="5" y="10" solution="L"></cell>
<cell x="5" y="11" type="block"></cell>
<cell x="5" y="12" solution="H"></cell>
<cell x="5" y="13" type="block"></cell>
<cell x="5" y="14" solution="I"></cell>
<cell x="5" y="15" type="block"></cell>
<cell x="6" y="1" solution="D" number="3"></cell>
<cell x="6" y="2" solution="I"></cell>
<cell x="6" y="3" solution="W"></cell>
<cell x="6" y="4" solution="A" number="11"></cell>
<cell x="6" y="5" solution="L"></cell><cell x="6" y="6" solution="I"></cell><cell x="6" y="7" type="block"></cell><cell x="6" y="8" solution="A" number="16"></cell><cell x="6" y="9" solution="C"></cell><cell x="6" y="10" solution="I"></cell><cell x="6" y="11" solution="D"></cell>
<cell x="6" y="12" solution="T"></cell><cell x="6" y="13" solution="E"></cell><cell x="6" y="14" solution="S"></cell><cell x="6" y="15" solution="T"></cell><cell x="7" y="1" type="block"></cell><cell x="7" y="2" solution="S"></cell><cell x="7" y="3" type="block"></cell><cell x="7" y="4" solution="N"></cell>
<cell x="7" y="5" type="block"></cell><cell x="7" y="6" type="block"></cell><cell x="7" y="7" type="block"></cell><cell x="7" y="8" solution="L"></cell><cell x="7" y="9" type="block"></cell><cell x="7" y="10" solution="S"></cell><cell x="7" y="11" type="block"></cell>
<cell x="7" y="12" solution="E"></cell><cell x="7" y="13" type="block"></cell><cell x="7" y="14" type="block"></cell><cell x="7" y="15" type="block"></cell><cell x="8" y="1" solution="C" number="4"></cell><cell x="8" y="2" solution="H"></cell><cell x="8" y="3" solution="I"></cell>
<cell x="8" y="4" solution="C"></cell><cell x="8" y="5" solution="K"></cell><cell x="8" y="6" solution="E" number="14"></cell><cell x="8" y="7" solution="N"></cell><cell x="8" y="8" type="block"></cell><cell x="8" y="9" solution="C" number="19"></cell><cell x="8" y="10" solution="H"></cell>
<cell x="8" y="11" solution="E"></cell><cell x="8" y="12" solution="N"></cell><cell x="8" y="13" solution="N"></cell><cell x="8" y="14" solution="A" number="26"></cell><cell x="8" y="15" solution="I"></cell><cell x="9" y="1" type="block"></cell><cell x="9" y="2" type="block"></cell>
<cell x="9" y="3" type="block"></cell><cell x="9" y="4" solution="H"></cell><cell x="9" y="5" type="block"></cell><cell x="9" y="6" solution="L"></cell><cell x="9" y="7" type="block"></cell><cell x="9" y="8" solution="C" number="17"></cell><cell x="9" y="9" type="block"></cell>
<cell x="9" y="10" type="block"></cell><cell x="9" y="11" type="block"></cell><cell x="9" y="12" solution="E"></cell><cell x="9" y="13" type="block"></cell><cell x="9" y="14" solution="B"></cell><cell x="9" y="15" type="block"></cell><cell x="10" y="1" solution="M" number="5"></cell>
<cell x="10" y="2" solution="O" number="9"></cell><cell x="10" y="3" solution="N"></cell><cell x="10" y="4" solution="O"></cell><cell x="10" y="5" solution="L"></cell><cell x="10" y="6" solution="I"></cell><cell x="10" y="7" solution="T"></cell><cell x="10" y="8" solution="H"></cell>
<cell x="10" y="9" type="block"></cell><cell x="10" y="10" solution="N" number="22"></cell><cell x="10" y="11" solution="E"></cell><cell x="10" y="12" solution="R"></cell><cell x="10" y="13" solution="U"></cell><cell x="10" y="14" solution="D"></cell><cell x="10" y="15" solution="A"></cell>
<cell x="11" y="1" type="block"></cell><cell x="11" y="2" solution="H"></cell><cell x="11" y="3" type="block"></cell><cell x="11" y="4" solution="R"></cell><cell x="11" y="5" type="block"></cell><cell x="11" y="6" solution="G"></cell><cell x="11" y="7" type="block"></cell><cell x="11" y="8" solution="A"></cell><cell x="11" y="9" type="block"></cell><cell x="11" y="10" solution="A"></cell>
<cell x="11" y="11" type="block"></cell><cell x="11" y="12" type="block"></cell><cell x="11" y="13" type="block"></cell><cell x="11" y="14" solution="U"></cell><cell x="11" y="15" type="block"></cell><cell x="12" y="1" solution="P" number="6"></cell><cell x="12" y="2" solution="E"></cell><cell x="12" y="3" solution="T"></cell><cell x="12" y="4" solution="I"></cell><cell x="12" y="5" solution="T"></cell>
<cell x="12" y="6" solution="I"></cell><cell x="12" y="7" solution="O"></cell><cell x="12" y="8" solution="N"></cell><cell x="12" y="9" solution="E"></cell><cell x="12" y="10" solution="D"></cell><cell x="12" y="11" type="block"></cell><cell x="12" y="12" solution="D" number="24"></cell><cell x="12" y="13" solution="U"></cell><cell x="12" y="14" solution="C"></cell><cell x="12" y="15" solution="K"></cell>
<cell x="13" y="1" type="block"></cell><cell x="13" y="2" solution="N"></cell><cell x="13" y="3" type="block"></cell><cell x="13" y="4" solution="T"></cell><cell x="13" y="5" type="block"></cell><cell x="13" y="6" solution="B"></cell><cell x="13" y="7" type="block"></cell><cell x="13" y="8" solution="G"></cell><cell x="13" y="9" type="block"></cell><cell x="13" y="10" solution="I"></cell>
<cell x="13" y="11" type="block"></cell><cell x="13" y="12" solution="I"></cell><cell x="13" y="13" type="block"></cell><cell x="13" y="14" solution="T"></cell><cell x="13" y="15" type="block"></cell><cell x="14" y="1" solution="O" number="7"></cell><cell x="14" y="2" solution="R"></cell>
<cell x="14" y="3" solution="W"></cell><cell x="14" y="4" solution="E"></cell><cell x="14" y="5" solution="L"></cell><cell x="14" y="6" solution="L"></cell><cell x="14" y="7" type="block"></cell><cell x="14" y="8" solution="E" number="18"></cell><cell x="14" y="9" solution="N"></cell>
<cell x="14" y="10" solution="N"></cell><cell x="14" y="11" solution="O"></cell><cell x="14" y="12" solution="B"></cell><cell x="14" y="13" solution="L"></cell><cell x="14" y="14" solution="E"></cell><cell x="14" y="15" solution="D"></cell><cell x="15" y="1" type="block"></cell><cell x="15" y="2" solution="Y"></cell><cell x="15" y="3" type="block"></cell><cell x="15" y="4" solution="S"></cell>
<cell x="15" y="5" type="block"></cell><cell x="15" y="6" solution="E"></cell><cell x="15" y="7" type="block"></cell><cell x="15" y="8" solution="S"></cell><cell x="15" y="9" type="block"></cell><cell x="15" y="10" solution="E"></cell><cell x="15" y="11" type="block"></cell><cell x="15" y="12" solution="S"></cell><cell x="15" y="13" type="block"></cell><cell x="15" y="14" solution="D"></cell>
<cell x="15" y="15" type="block"></cell></grid>
<word id="1" x="1-8" y="2" solution="side dish"></word>
<word id="2" x="10-15" y="2"></word>
<word id="3" x="1-4" y="4"></word>
<word id="4" x="6-15" y="4"></word>
<word id="5" x="1-6" y="6" solution="mumbai duck"><cells x="12" y="12-15"></cells></word>
<word id="6" x="8-15" y="6"></word>
<word id="7" x="1-7" y="8" solution="nominal changes"><cells x="9-15" y="8"></cells></word>
<word id="8" x="1-8" y="10"></word>
<word id="9" x="10-15" y="10"></word>
<word id="10" x="1-10" y="12"></word>
<word id="11" x="12-15" y="12"></word>
<word id="12" x="1-6" y="14"></word>
<word id="13" x="8-15" y="14"></word>
<word id="14" x="2" y="1-8"></word>
<word id="15" x="4" y="1-4"></word>
<word id="16" x="6" y="1-6"></word>
<word id="17" x="8" y="1-7" solution="chicken chennai"><cells x="8" y="9-15"></cells></word>
<word id="18" x="10" y="1-8"></word>
<word id="19" x="12" y="1-10"></word>
<word id="20" x="14" y="1-6"></word>
<word id="21" x="4" y="6-15"></word>
<word id="22" x="6" y="8-15" solution="acid test"></word>
<word id="23" x="14" y="8-15"></word>
<word id="24" x="2" y="10-15"></word>
<word id="25" x="10" y="10-15"></word>
<clues ordering="normal"><title><b>Across</b></title>
<clue word="1" number="8" format="4,4">Players collectively demolish extra food</clue>
<clue word="2" number="9" format="6">Old king&#39;s literary pseudonym</clue>
<clue word="3" number="10" format="4">Name of man backing another in Spanish city</clue>
<clue word="4" number="11" format="10">Solitary types disoriented in chain store</clue>
<clue word="5" number="12,24down" format="6,4">Mother has to purchase, we hear, dear kind of fish</clue>
<clue word="6" number="14" format="8">Fit for match between the Spanish and the French, one great back</clue>
<clue word="7" number="15,17" format="7,7">No real alterations seen in 2, 7, 9, 10, 12, 13, 19, 22 across and 22 down</clue>
<clue word="8" number="20" format="8">It&#39;s bad, tucking into something to eat - very bad</clue>
<clue word="9" number="22" format="6">Name Dianne differently</clue>
<clue word="10" number="23" format="10">Scary thing, Frenchman turning on fellow conservative</clue>
<clue word="11" number="24" format="4">Money deposited in bank safe, but only to begin with</clue>
<clue word="12" number="25" format="6">Article by informal relative becoming academic test</clue>
<clue word="13" number="26" format="8">Wrongly removed tube buried in one part of garden</clue></clues>
<clues ordering="normal"><title><b>Down</b></title>
<clue word="14" number="1" format="8">Direction to slow down tune trio ruined</clue>
<clue word="15" number="2" format="4">New name given Jane, after moving east</clue>
<clue word="16" number="3" format="6">One rule I had set up for Indian festival</clue>
<clue word="17" number="4,19" format="7,7">Fearful hen I can, oddly, put in kind of curry</clue>
<clue word="18" number="5" format="8">Stone block with solid middle installed in part of year</clue>
<clue word="19" number="6" format="10">Dainty little daughter covering one leg, as requested</clue>
<clue word="20" number="7" format="6">What Blair became before spring</clue>
<clue word="21" number="13" format="10">Asian citizen I see being mistreated around judge</clue>
<clue word="22" number="16" format="4,4">Bill that is, over time, providing a crucial check</clue>
<clue word="23" number="18" format="8">Maid of Orleans uplifted, guided and elevated</clue>
<clue number="19" is-link="1" word="17">See 4</clue>
<clue word="24" number="21" format="6">They are mostly awfully coarse</clue>
<clue number="24" is-link="1" word="5">See 12</clue></clues>
</crossword></rectangular-puzzle></crossword-compiler>
"""
		self.extractor = CrosswordDotInfoXmlExtractor()

	def test_should_extract_title_from_xml(self):
		self.extractor.parse(self.xml)
		self.assertEqual(self.extractor.title(), 'gdn.quick')

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

if __name__ == '__main__':
	unittest.main()
