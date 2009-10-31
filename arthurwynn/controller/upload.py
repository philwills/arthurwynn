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
			self.redirect('/' + crossword.type + '/' + str(crossword.number))

class LegacyCrosswordUploadPage(ModelAndViewPage):
	def __init__(self):
		self.extractor = GuCrosswordXmlExtractor()
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
		crossword.size(self.extractor.width())
		crossword.across_x = self.extractor.across_x()
		crossword.down_x = self.extractor.down_x()
		crossword.across_y = self.extractor.across_y()
		crossword.down_y = self.extractor.down_y()
		crossword.across_nums = self.extractor.across_nums()
		crossword.down_nums = self.extractor.down_nums()
		crossword.across_clues = self.extractor.across_clues()
		crossword.down_clues = self.extractor.down_clues()
		crossword.across_solutions = self.extractor.across_solutions()
		crossword.down_solutions = self.extractor.down_solutions()
		crossword.xml = xml
		self.repository.add_or_update(crossword)
		if (self.response):
			self.redirect('/' + crossword.type + '/' + str(crossword.number))

