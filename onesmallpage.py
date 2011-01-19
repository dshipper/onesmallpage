import os
from google.appengine.ext.webapp import template
import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import mail
import urllib
import re
import Book
import Reader


html_pattern = r"<dcterms:hasFormat rdf:resource=\"(?P<url>[^<]+(htm|html)[^<])<"
chtml_pattern = re.compile(html_pattern)

class Daemon_1(webapp.RequestHandler):
	def get(self):
		#get every reader
		readers = Reader.Reader.all()
		print 'Content-Type: text/plain'
		print ''
		for reader in readers:
			etext_number = reader.etext_number
			query = Book.Book.all().filter("etext_number = ",etext_number)
			book = query[0]
			if(book.html_url == None or book.html_url == "" or book.html_url == 0):
				#we have to grab the html_url
				etext_url = book.etext_url
				f = urllib.urlopen(etext_url)
				
				html = f.read()
				f.close()
				html_match = chtml_pattern.search(str(html))
				if(html_match == None):
					print "Error. URL is."
				else:
					html_url = html_match.group('url')
					book.html_url = html_url
					book.put()
			else:
				html_url = book.html_url			
			user_address = reader.email
			sender_address = "dshipper@gmail.com"
			subject = "One Page of Your Book: " + book.title 
			body = "Thank you for registering with us."
			
			print 'Hello, world!'
			try:
				mail.send_mail(sender_address, user_address, subject, body)
			except:
				print 'error'

class Daemon_2(webapp.RequestHandler):
	def get(self):
		#get every reader
		readers = Reader.Reader.all().filter("emails_per_day > 1")
		for reader in readers:	
			user_address = reader.email
			sender_address = "dshipper@gmail.com"
			subject = "Confirm your registration"
			body = "Thank you for registering with us."
			print 'Content-Type: text/plain'
			print ''
			print 'Hello, world!'
			try:
				mail.send_mail(sender_address, user_address, subject, body)
			except:
				print 'error'
				
class Daemon_3(webapp.RequestHandler):
	def get(self):
		#get every reader
		readers = Reader.Reader.all().filter("emails_per_day > 2")
		for reader in readers:	
			user_address = reader.email
			sender_address = "dshipper@gmail.com"
			subject = "Confirm your registration"
			body = "Thank you for registering with us."
			print 'Content-Type: text/plain'
			print ''
			print 'Hello, world!'
			try:
				mail.send_mail(sender_address, user_address, subject, body)
			except:
				print 'error'
				
class Daemon_4(webapp.RequestHandler):
	def get(self):
		#get every reader
		readers = Reader.Reader.all().filter("emails_per_day > 3")
		for reader in readers:	
			user_address = reader.email
			sender_address = "dshipper@gmail.com"
			subject = "Confirm your registration"
			body = "Thank you for registering with us."
			print 'Content-Type: text/plain'
			print ''
			print 'Hello, world!'
			try:
				mail.send_mail(sender_address, user_address, subject, body)
			except:
				print 'error'

class Daemon_5(webapp.RequestHandler):
	def get(self):
		#get every reader
		readers = Reader.Reader.all().filter("emails_per_day > 4")
		for reader in readers:	
			user_address = reader.email
			sender_address = "dshipper@gmail.com"
			subject = "Confirm your registration"
			body = "Thank you for registering with us."
			print 'Content-Type: text/plain'
			print ''
			print 'Hello, world!'
			try:
				mail.send_mail(sender_address, user_address, subject, body)
			except:
				print 'error'

class AddReader(webapp.RequestHandler):
	def get(self):
		etext_number = self.request.get('etext')
		email = self.request.get('email')
		times = self.request.get('times')
		#TODO: check TIMES
		#make sure this dood doesn't already have a reader account
		reader = Reader.Reader()
		reader.email = email
		reader.emails_per_day = int(times)
		reader.etext_number = etext_number
		reader.position = 0
		reader.put()
		path = os.path.join(os.path.dirname(__file__), 'addreader.html')
		self.response.out.write(template.render(path, None))
		

class StartPage(webapp.RequestHandler):
	def get(self):
		etext_number = self.request.get('etext')
		template_values = {
			'etext':etext_number
		}
		path = os.path.join(os.path.dirname(__file__), 'start.html')
		self.response.out.write(template.render(path, template_values))

class MainPage(webapp.RequestHandler):
	def get(self):
		template_values = {
        }
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

class SearchPage(webapp.RequestHandler):
	def get(self):
		query = self.request.get('q')
		query_split = query.split(" ")
		if(len(query_split) == 0):
			author_first_name = "0"
			author_last_name = "0"
		elif(len(query_split) > 2):
			author_first_name = query[0] + query[1]
			author_last_name = query[2]
		else:
			author_first_name = query[0]
			author_last_name = query[1]
	
		books_by_title = Book.Book.all().filter("title =",str(query))
		books_by_first_name = Book.Book.all().filter("author_first_name =",str(query))
		books_by_last_name = Book.Book.all().filter("author_last_name =", str(query))
		books_by_both = Book.Book.all().filter("author_full_name =", str(query))
		books = []
		
		for book in books_by_title:
			link = "<a href='/start?etext="+book.etext_number+"'>Start Reading this Book Now.</a>" 
			books.append(book.title + " by " + book.author_first_name + " " + book.author_last_name + " " + link) 

		for book in books_by_first_name:
			link = "<a href='/start?etext="+book.etext_number+"'>Start Reading this Book Now.</a>" 
			books.append(book.title + " by " + book.author_first_name + " " + book.author_last_name + " " + link) 

		for book in books_by_last_name:
			link = "<a href='/start?etext="+book.etext_number+"'>Start Reading this Book Now.</a>" 
			books.append(book.title + " by " + book.author_first_name + " " + book.author_last_name + " " + link)
	
		for book in books_by_both:
			link = "<a href='/start?etext="+book.etext_number+"'>Start Reading this Book Now.</a>" 
			books.append(book.title + " by " + book.author_first_name + " " + book.author_last_name + " " + link)


		template_values = {
            'books':books
        }
		path = os.path.join(os.path.dirname(__file__), 'search.html')
		self.response.out.write(template.render(path, template_values))



application = webapp.WSGIApplication(
                          [('/', MainPage), ('/search', SearchPage), ('/start', StartPage), ("/add-reader", AddReader), ("/daemon-1", Daemon_1), ("/daemon-2", Daemon_2), ("/daemon-3", Daemon_3), ("/daemon-4", Daemon_4), ("/daemon-5", Daemon_5)],
                          debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
