from arthurwynn.controller.modelview import ModelAndViewPage

from arthurwynn.crossword import *

from xml.etree.ElementTree import fromstring

class CrosswordUploadPage(ModelAndViewPage):
	def get(self):
		self.render('crosswordupload', {})
	
	def post(self):
		crossword = Crossword()
		extractor = CrosswordDotInfoXmlExtractor(self.request.get('xml'))
		crossword.name = extractor.title()
		crossword.type = extractor.type()
		crossword.creator = extractor.creator()
		crossword.number = extractor.identifier()
		crossword.size(extractor.width())
		crossword.build_solution(extractor.letters())
		crossword.build_clues(extractor.across_clues(), extractor.down_clues())
		crossword.put()
		self.redirect('/crossword?key=' + str(crossword.key()))

class CrosswordDotInfoXmlExtractor():
	def __init__(self, xmlString):
		self.root = fromstring(xmlString)
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
