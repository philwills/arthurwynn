from crossword import *

from google.appengine.ext import db

class UserCrossword(db.Model):
	user = db.UserProperty()
	crossword = db.ReferenceProperty(Crossword)
	answers = db.StringProperty()
	created = db.DateTimeProperty(auto_now_add=True)
