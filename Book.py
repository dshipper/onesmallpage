from google.appengine.ext import db

class Book(db.Model):
	title = db.StringProperty()
	author_full_name = db.StringProperty()
	#date_published = db.StringPropert()
	etext_number = db.StringProperty()
	etext_url = db.StringProperty()
	html_url = db.StringProperty()
	
