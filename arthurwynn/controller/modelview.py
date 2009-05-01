import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class ModelAndViewPage(webapp.RequestHandler):
	def render(self, view, model={}):
		path = os.path.join(os.path.dirname(__file__), '../../template', view)
		self.response.out.write(template.render(path + '.tpl', model))
