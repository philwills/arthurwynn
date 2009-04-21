from arthurwynn.controller.modelview import ModelAndViewPage

from arthurwynn.crossword import Crossword

class CrosswordListPage(ModelAndViewPage):
	def get(self):
		crosswords = Crossword.all().order("-date").fetch(10)
		model = {
			'crosswords': crosswords,
		}
		self.render('crosswordlist', model)

class CrosswordAtomPage(ModelAndViewPage):
	def get(self):
		crosswords = Crossword.all().order("-date").fetch(10)
		model = {
			'crosswords': crosswords,
			'latestdate': crosswords[0].date,
		}
		self.render('crossword_atom', model)
