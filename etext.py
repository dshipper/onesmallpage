import os
from google.appengine.ext.webapp import template
import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app 
from google.appengine.ext import db   

import re, codecs, urllib, logging
import Book
	
class BulkDisplay(webapp.RequestHandler):
	def get(self):
		books = db.GqlQuery("SELECT * FROM Book LIMIT 10")
		for book in books:
			self.response.out.write("Book found. Title: " + book.title + ". Author: " + book.author_first_name + " " + book.author_last_name)

class BulkLoad(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write("Hello!")
		logging.debug("Here")

		etext_pattern = r"<pgterms:etext.*\"[a-zA-Z]+(?P<etext_number>\d+)\""
		title_pattern = r"title.*>(?P<title>.*)<"
		author_pattern = r"creator.*>(?P<author>.*)<"
		friendly_pattern = r"friendly.*>(?P<friendly>.*)<"
		html_pattern = r"<dcterms:hasFormat rdf:resource=\"(?P<url>[^<]+(htm|html))"
		cetext_pattern = re.compile(etext_pattern)
		ctitle_pattern = re.compile(title_pattern)
		cauthor_pattern = re.compile(author_pattern)
		cfriendly_pattern = re.compile(friendly_pattern)
		chtml_pattern = re.compile(html_pattern)
		file = codecs.open("static/catalog.rdf", "r", encoding="iso-8859-1")

		NONE = 0
		ETEXT = 1
		TITLE = 2
		AUTHOR = 3
		FRIENDLY = 4

		state = NONE #haven't found anything
		
		title = ""
		author = ""
		author_full_name = ""
		author_first_name = ""
		author_last_name = ""
		etext = ""
		friendly = ""
		
		t = file.readline()
		
		record = 1
		while(t != None and record < 24000):
			if(state == NONE):
				title = ""
				author = ""
				etext = ""
				friendly = ""
				match = cetext_pattern.search(t)
				if (match):
					#print("Found etext match.")
					#print("Etext number: " + match.group('etext_number'))
					state = ETEXT
					etext = match.group('etext_number')
			elif(state == ETEXT):
				match = ctitle_pattern.search(t)
				if(match):
					#print ("Found title.")
					#print("Title: " + match.group('title'))
					state = AUTHOR
					title = match.group('title')
			elif(state == AUTHOR):					
				match = cauthor_pattern.search(t)
				if(match):
				#print("Found author.")
				#print("Author: " + match.group('author'))
					state = FRIENDLY
					author = match.group('author')
					words = author.split(',')
						#self.response.out.write(words)
					if(len(words) > 1):
						author_first_name = words[1].strip()
						author_last_name = words[0].strip()
					else:
						author_first_name = words[0].strip()
					author_full_name = author_first_name + " " + author_last_name
			elif(state == FRIENDLY):
				match = cfriendly_pattern.search(t)
				if(match):
					#print("Found friendly.")
					#print("Friendly: " + match.group('friendly'))
					state = NONE
					friendly = match.group('friendly')
		
					#now lets get the url to find the book text
					url = "http://www.gutenberg.org/cache/epub/" + etext + "/pg" + etext + ".rdf"

	
					new_book = Book.Book()
					new_book.title = title
					new_book.author_first_name = author_first_name
					new_book.author_last_name = author_last_name
					new_book.etext_number = etext
					new_book.etext_url = url
					new_book.author_full_name = author_full_name
					new_book.put()
					if((record % 100) == 0): 
						self.response.out.write("Wrote record number " + str(record))
					record += 1
						
			try: 
				t = file.readline()
			except:
				t = None
		


application = webapp.WSGIApplication(
	[('/admin/bulk-load', BulkLoad),
	 ('/admin/bulk-display', BulkDisplay)],
	debug=True
					)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
