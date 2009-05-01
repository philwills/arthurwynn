from arthurwynn.controller.modelview import ModelAndViewPage
from arthurwynn.controller.display import CrosswordPage

from google.appengine.ext import db

from arthurwynn.crossword import *

class CrosswordCreationPage(ModelAndViewPage):
	def get(self):
		self.render('crosswordcreate')
		
	def post(self):
		crossword = Crossword()
		crossword.size(int(self.request.get('size')))
		crossword.name = self.request.get('name')
		crossword.put()
		self.redirect('/create/grid?key=' + str(crossword.key()))

class CrosswordGridPage(CrosswordPage):
	def get_view_name(self):
		return 'crosswordgrid'

	def post(self):
		crossword = db.get(db.Key(self.request.get('key')))
		argument_names = self.request.arguments()
		letters = {}
		for argument_name in argument_names:
			if argument_name != 'key' and argument_name != 'submit':
				x, y = argument_name.split('-')
				letters[int(x), int(y)] = self.request.get(argument_name)
		crossword.build_solution(letters)
		crossword.put()
		self.redirect('/create/clues?key=' + str(crossword.key()))

class CrosswordCluePage(CrosswordPage):
	def get_view_name(self):
		return 'crosswordclues'

	def post(self):
		crossword = db.get(db.Key(self.request.get('key')))
		across_clues = {}
		down_clues = {}
		argument_names = self.request.arguments()
		for argument_name in argument_names:
			if argument_name.find('-') > 0:
				number, direction = argument_name.split('-')
				if direction == 'across':
					across_clues[number] = self.request.get(argument_name)
				if direction == 'down':
					down_clues[number] = self.request.get(argument_name)
		crossword.build_clues(across_clues, down_clues)
		crossword.put()
		self.redirect('/crossword?key=' + str(crossword.key()))
