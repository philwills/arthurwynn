from arthurwynn.controller.modelview import ModelAndViewPage
from arthurwynn.controller.upload import CrosswordUploadPage, LegacyCrosswordUploadPage
from arthurwynn.controller.create import CrosswordCreationPage, CrosswordGridPage, CrosswordCluePage
from arthurwynn.controller.display import CrosswordPage, MicroappCrosswordPage, BlindCrosswordPage, AnagramPage
from arthurwynn.controller.list import CrosswordListPage, CrosswordAtomPage, MicroappLatestPage

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from arthurwynn.crossword import *

template.register_template_library('common.filters')

application = webapp.WSGIApplication([
									('/', CrosswordListPage),
									('/crossword', CrosswordPage),
									(r'/(.*)/latest', MicroappLatestPage),
									(r'/(.*)/(.*)/blind', BlindCrosswordPage),
									('/anagram', AnagramPage),
                                    ('/create', CrosswordCreationPage),
                                    ('/create/grid', CrosswordGridPage),
                                    ('/create/clues', CrosswordCluePage),
                                    ('/upload', CrosswordUploadPage),
                                    ('/upload/legacy', LegacyCrosswordUploadPage),
                                    ('/atom.xml', CrosswordAtomPage),
									(r'/(.*)/(.*)', MicroappCrosswordPage),
									], debug=True)
		
def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
