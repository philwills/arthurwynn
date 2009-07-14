from crossword import Crossword

class CrosswordRepository():
	def create(self):
		return Crossword()

	def find(self, type, number):
		crosswords = Crossword.all().filter("type =", type).filter("number =", int(number)).fetch(limit=1)
		if len(crosswords) > 0:
			return crosswords[0]
		return None

	def latest(self, type):
		crosswords = Crossword.all().filter("type =", type).order("-date").fetch(limit=1)
		if len(crosswords) > 0:
			return crosswords[0]
		return None


	def add_or_update(self, crossword):
		crossword.put()
