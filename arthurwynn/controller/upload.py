from arthurwynn.controller.modelview import ModelAndViewPage

from arthurwynn.crossword import *
from arthurwynn.crossword_repository import CrosswordRepository

from xml.etree.ElementTree import fromstring

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

class CrosswordDotInfoXmlExtractor():
	def parse(self, xml_string):
		self.root = fromstring(xml_string)
		self.namespace = '{http://crossword.info/xml/rectangular-puzzle}'
		self.puzzle = self.root.find('./' + self.namespace + 'rectangular-puzzle/')
		self.grid = self.puzzle.find('./' + self.namespace + 'crossword/' + self.namespace + 'grid')
		self.across_clue_dict = {}
		self.down_clue_dict = {}
		self.extract_clues()

	def title(self):
		return self.puzzle.find('./' + self.namespace + 'metadata/' + self.namespace + 'title').text

	def type(self):
		titleText = self.title()
		if titleText[0:4] == 'gdn.':
			return titleText[4:]

	def creator(self):
		return self.puzzle.find('./' + self.namespace + 'metadata/' + self.namespace + 'creator').text
		
	def identifier(self):
		return int(self.puzzle.find('./' + self.namespace + 'metadata/' + self.namespace + 'identifier').text)
		
	def width(self):
		return int(self.grid.get('width'))
		
	def height(self):
		return int(self.grid.get('height'))

	def letters(self):
		letters = {}
		for cell in self.grid.findall('./' + self.namespace + 'cell'):
			if cell.get('solution'):
				letters[int(cell.get('x')), int(cell.get('y'))] = cell.get('solution')
			else:
				letters[int(cell.get('x')), int(cell.get('y'))] = ''
		return letters

	def across_clues(self):
		return self.across_clue_dict

	def down_clues(self):
		return self.down_clue_dict

	def extract_clues(self):
		for clues in self.puzzle.findall('./' + self.namespace + 'crossword/' + self.namespace + 'clues'):
			if (clues.find('./' + self.namespace + 'title/' + self.namespace +'b').text == 'Across'):
				for clue in clues.findall('./' + self.namespace + 'clue'):
					self.across_clue_dict[clue.get('number')] = clue.text + ' (' + clue.get('format') + ')'
			else:
				for clue in clues.findall('./' + self.namespace + 'clue'):
					self.down_clue_dict[clue.get('number')] = clue.text + ' (' + clue.get('format') + ')'
