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

if __name__ == '__main__':
	unittest.main()
