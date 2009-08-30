from arthurwynn.controller.modelview import ModelAndViewPage

from arthurwynn.crossword import *
from arthurwynn.crossword_repository import CrosswordRepository

from extractor import *

class CrosswordUploadPage(ModelAndViewPage):
	def __init__(self):
		self.extractor = CrosswordDotInfoXmlExtractor()
		self.repository = CrosswordRepository()

	def get(self):
		self.render('crosswordupload', {})
	
	def post(self):
		xml = self.request.get('xml')
		self.extractor.parse(xml)
		type = self.extractor.type()
		number = self.extractor.identifier()
		crossword = self.repository.find(type, number)
		if crossword is None:
			crossword = self.repository.create()
			crossword.type = type
			crossword.number = number
		crossword.name = self.extractor.title()
		crossword.creator = self.extractor.creator()
		crossword.size(self.extractor.width())
		crossword.build_solution(self.extractor.letters())
		crossword.build_clues(self.extractor.across_clues(), self.extractor.down_clues())
		crossword.xml = xml.decode('utf-8')
		self.repository.add_or_update(crossword)
		if (self.response):
			self.redirect('/microapp/resources/' + crossword.type + '/' + str(crossword.number))
