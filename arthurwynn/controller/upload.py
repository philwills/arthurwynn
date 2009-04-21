import cgi
import os

from arthurwynn.controller.modelview import ModelAndViewPage

from arthurwynn.crossword import *

from xml.etree.ElementTree import *

class CrosswordUploadPage(ModelAndViewPage):
	def get(self):
		self.render('crosswordupload', {})
	
	def post(self):
		crossword = Crossword()
		root = fromstring(self.request.get('xml'))
		namespace = '{http://crossword.info/xml/rectangular-puzzle}'
		puzzle = root.find('./' + namespace + 'rectangular-puzzle/')
		title = puzzle.find('./' + namespace + 'metadata/' +namespace + 'title')
		crossword.name = title.text
		if title.text[0:4] == 'gdn.':
			crossword.type = title.text[4:]
		creator = puzzle.find('./' + namespace + 'metadata/' +namespace + 'creator')
		crossword.creator = creator.text
		identifier = puzzle.find('./' + namespace + 'metadata/' +namespace + 'identifier')
		crossword.number = int(identifier.text)
		grid = puzzle.find('./' + namespace + 'crossword/' +namespace + 'grid')
		crossword.size(int(grid.get('width')))
		letters = {}
		for cell in grid.findall('./' + namespace + 'cell'):
			if cell.get('solution'):
				letters[int(cell.get('x')), int(cell.get('y'))] = cell.get('solution')
			else:
				letters[int(cell.get('x')), int(cell.get('y'))] = ''
		crossword.build_solution(letters)
		across_clues = {}
		down_clues = {}
		for clues in puzzle.findall('./' + namespace + 'crossword/' + namespace + 'clues'):
			if (clues.find('./' + namespace + 'title/' + namespace +'b').text == 'Across'):
				for clue in clues.findall('./' + namespace + 'clue'):
					across_clues[clue.get('number')] = clue.text + ' (' + clue.get('format') + ')'
			else:
				for clue in clues.findall('./' + namespace + 'clue'):
					down_clues[clue.get('number')] = clue.text + ' (' + clue.get('format') + ')'
		crossword.build_clues(across_clues, down_clues)
		crossword.put()
		self.redirect('/crossword?key=' + str(crossword.key()))
