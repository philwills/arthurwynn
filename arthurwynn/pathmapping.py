from arthurwynn.controller.modelview import ModelAndViewPage
from arthurwynn.controller.upload import CrosswordUploadPage
from arthurwynn.controller.create import CrosswordCreationPage, CrosswordGridPage, CrosswordCluePage
from arthurwynn.controller.display import CrosswordPage, MicroappCrosswordPage, BlindCrosswordPage
from arthurwynn.controller.list import CrosswordListPage, CrosswordAtomPage, MicroappLatestPage

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from arthurwynn.crossword import *

template.register_template_library('common.filters')

application = webapp.WSGIApplication([
									('/', CrosswordListPage),
									('/crossword', CrosswordPage),
									(r'/microapp/component/(.*)/latest', MicroappLatestPage),
									(r'/microapp/resources/(.*)/(.*)/blind', BlindCrosswordPage),
									(r'/microapp/resources/(.*)/(.*)', MicroappCrosswordPage),
                                    ('/create', CrosswordCreationPage),
                                    ('/create/grid', CrosswordGridPage),
                                    ('/create/clues', CrosswordCluePage),
                                    ('/upload', CrosswordUploadPage),
                                    ('/atom.xml', CrosswordAtomPage),
									], debug=True)
		
def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
