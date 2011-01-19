from google.appengine.ext import db

class Reader(db.Model):
	email = db.StringProperty()
	emails_per_day = db.IntegerProperty()
	etext_number = db.StringProperty()
	position = db.IntegerProperty()