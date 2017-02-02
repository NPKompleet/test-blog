#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
from google.appengine.ext import db

jinja_environment = jinja2.Environment(autoescape=True,loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

#"""
class Content(db.Model):
    title= db.StringProperty(required=True)
    content= db.TextProperty(required=True)
    datetime= db.DateTimeProperty(auto_now_add=True)
    artificial_tag= bool
    programming_tag= bool
    graphics_tag= bool
    networking_tag= bool
    total_tags= db.TextProperty(required=True)


class Quotes(db.Model):
    quote=db.TextProperty(required=True)
    author=db.StringProperty(required=True)


class Books(db.Model):
    pass


class Education(db.Model):
    pass


#"""

class AdminHandler(webapp2.RequestHandler):
    def write(self, values):
        template = jinja_environment.get_template('admin.html')
        self.response.write(template.render(values))

    def get(self):
        template_values = {
            "quote":"--quote--",
            "author":"--author--",
            "error":""}
        #template = jinja_environment.get_template('admin.html')
        #self.response.write(template.render(template_values))
        self.write(template_values)

    def post(self):
        quote= self.request.get("quote")
        author= self.request.get("author")
        if quote==None or quote=="--quote--" or author==None or author=="--author--":
            error="Sorry must insert Values"
            template_values = {
            "quote":quote,
            "author":author,
            "error":error}
            #template = jinja_environment.get_template('admin.html')
            #self.response.write(template.render(template_values))
            self.write(template_values)

        else:
            q=Quotes(quote=quote, author=author)
            q.put()
            self.redirect("/admin")

            

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = jinja_environment.get_template('thoth.html')
        self.response.write(template.render())
        #self.response.write(self.request)


class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = jinja_environment.get_template('about.html')
        self.response.write(template.render())



class BookHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = jinja_environment.get_template('books.html')
        self.response.write(template.render())


class QuoteHandler(webapp2.RequestHandler):  
    def get(self):
        #quotes =db.GqlQuery("DELETE * from Quotes WHERE author= Mark Twain")
        quotes =db.GqlQuery("SELECT * from Quotes")
        template_values = {"quotes":quotes}
        template = jinja_environment.get_template('quotes.html')
        self.response.write(template.render(template_values))
                            



class EducationHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = jinja_environment.get_template('education.html')
        self.response.write(template.render())




class PortfolioHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = jinja_environment.get_template('portfolio.html')
        self.response.write(template.render())



class DownloadHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = jinja_environment.get_template('downloads.html')
        self.response.write(template.render())

        
app = webapp2.WSGIApplication([
    ('/', MainHandler),('/about', AboutHandler),
    ('/quotes', QuoteHandler),('/books', BookHandler),
    ('/portfolio', PortfolioHandler),('/education', EducationHandler),
    ('/downloads', DownloadHandler), ('/admin', AdminHandler)
], debug=True)
