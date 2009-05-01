from arthurwynn.controller.modelview import ModelAndViewPage

from google.appengine.ext import webapp

from arthurwynn.crossword import *
from arthurwynn.user_crossword import *

class SaveCrosswordState(webapp.RequestHandler):
	def post(self):
		pass
