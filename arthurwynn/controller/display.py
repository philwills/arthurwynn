from arthurwynn.controller.modelview import ModelAndViewPage

from google.appengine.ext import db

from arthurwynn.crossword import *

class CrosswordPage(ModelAndViewPage):
	def get(self):
		crossword = db.get(db.Key(self.request.get('key')))
		model = {
			'crossword': crossword,
		}
		self.render(self.get_view_name(), model)

	def get_view_name(self):
		return 'crossword'

class MicroappCrosswordPage(ModelAndViewPage):
	def get(self, type, number):
		crosswords = Crossword.all().filter("type =", type).filter("number =", int(number))
		model = {
			'crossword': crosswords[0],
		}
		self.render(self.get_view_name(), model)

	def get_view_name(self):
		return 'crossword'

class BlindCrosswordPage(MicroappCrosswordPage):
	def get_view_name(self):
		return 'blind'

