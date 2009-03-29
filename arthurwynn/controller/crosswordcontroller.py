import cgi
import os

from google.appengine.ext import db

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from arthurwynn.crossword import *
from arthurwynn.user_crossword import *

from xml.etree.ElementTree import *

class ModelAndViewPage(webapp.RequestHandler):
	def render(self, view, model={}):
		path = os.path.join(os.path.dirname(__file__), '../../template', view)
		self.response.out.write(template.render(path + '.tpl', model))

class CrosswordPage(ModelAndViewPage):
	def get(self):
		crossword = db.get(db.Key(self.request.get('key')))
		model = {
			'crossword': crossword,
		}
		self.render(self.get_view_name(), model)

	def get_view_name(self):
		return 'crossword'

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

class CrosswordListPage(ModelAndViewPage):
	def get(self):
		crosswords = Crossword.all().order("-date").fetch(10)
		model = {
			'crosswords': crosswords,
		}
		self.render('crosswordlist', model)

class SaveCrosswordState(webapp.RequestHandler):
	def post(self):
		pass

class CrosswordAtomPage(ModelAndViewPage):
	def get(self):
		crosswords = Crossword.all().order("-date").fetch(10)
		model = {
			'crosswords': crosswords,
			'latestdate': crosswords[0].date,
		}
		self.render('crossword_atom', model)

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

application = webapp.WSGIApplication([
									('/', CrosswordListPage),
									('/crossword', CrosswordPage),
                                    ('/create', CrosswordCreationPage),
                                    ('/create/grid', CrosswordGridPage),
                                    ('/create/clues', CrosswordCluePage),
                                    ('/upload', CrosswordUploadPage),
                                    ('/save', SaveCrosswordState),
                                    ('/atom.xml', CrosswordAtomPage),
									], debug=True)
		
def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
