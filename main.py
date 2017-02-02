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
import cgi
import json
import re
from google.appengine.ext import db

jinja_environment = jinja2.Environment(autoescape=True,loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
jinja_environment2 = jinja2.Environment(autoescape=False,loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

#"""

class ImageHandler(webapp2.RequestHandler):
    def get(self):
        #image = db.get(self.request.get("img_id"))
        B=self.request.get("img_id")
        image= db.GqlQuery("SELECT * from Image where name = '%s' " %B).fetch(1)
        if image[0].stored_image:
            self.response.headers['Content-Type'] = 'image/*'
            self.response.write(image[0].stored_image)
        else:
            self.response.write('No image')



class Image(db.Model):
    name=db.StringProperty(required=True)
    stored_image= db.BlobProperty()



class Content(db.Model):
    heading= db.StringProperty(required=True)
    content= db.TextProperty(required=True)
    datetime= db.DateTimeProperty(auto_now_add=True)
    artificial_tag= db.StringProperty(required=True)
    programming_tag= db.StringProperty(required=True)
    graphics_tag= db.StringProperty(required=True)
    networking_tag= db.StringProperty(required=True)
    databases_tag= db.StringProperty(required=True)
    algorithms_tag= db.StringProperty(required=True)
    computationalphysics_tag= db.StringProperty(required=True)
    total_tags= db.StringProperty()
    summary= db.TextProperty()
    link=db.StringProperty()


class Location(db.Model):
    acct= db.StringProperty(required=True)
    location= db.TextProperty(required=True)



class ContentHandler(webapp2.RequestHandler):
    def write(self, values):
        template = jinja_environment2.get_template('content.html')
        self.response.write(template.render(values))
    
    def get(self):
        B=self.request.get("link")
        content= db.GqlQuery("SELECT * from Content where link = '%s' " %B).fetch(1)
        template_values = {"content":content[0]}
        self.write(template_values)
        

    

class AdminContentHandler(webapp2.RequestHandler):
    def write(self, values):
        template = jinja_environment.get_template('admincontent.html')
        self.response.write(template.render(values))
    
    def get(self):
        template_values = {
            "content":"--content--",
            "heading":"--heading--",
            "totaltags":"--totaltags--",
            "summary":"--summary--",
            "error":""}
        self.write(template_values)
        

    def post(self):
        content=self.request.get("content")
        heading=self.request.get("heading")
        totaltags=self.request.get("total_tags")
        summary=self.request.get("summary")
            
        if content==None or content=="--content--" or heading==None or heading=="--heading--":
            error="Sorry must insert Values"
            template_values = {
            "content":content,
            "heading":heading,
            "totaltags":totaltags,
            "summary":summary,
            "error":error}
            
            self.write(template_values)

        else:
            artificial_tag= str(self.request.get("artificialtag")=="on")
            programming_tag= str(self.request.get("programmingtag")=="on")
            graphics_tag= str(self.request.get("graphicstag")=="on")
            networking_tag= str(self.request.get("networkingtag")=="on")
            databases_tag= str(self.request.get("databasestag")=="on")
            algorithms_tag= str(self.request.get("algorithmtag")=="on")
            total_tags= self.request.get("totaltags")
            summary=self.request.get("summary")
            link= heading.lower().replace(" ","-")
            
            c= Content(heading=heading, content=content, artificial_tag=artificial_tag,
                       programming_tag=programming_tag, graphics_tag=graphics_tag,
                       networking_tag=networking_tag, databases_tag=databases_tag,
                       algorithms_tag=algorithms_tag, total_tags=total_tags,
                       summary=summary, link=link)
            c.put()
        


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

##    def post(self):
##        quote= self.request.get("quote")
##        author= self.request.get("author")
##        if quote==None or quote=="--quote--" or author==None or author=="--author--":
##            error="Sorry must insert Values"
##            template_values = {
##            "quote":quote,
##            "author":author,
##            "error":error}
##            #template = jinja_environment.get_template('admin.html')
##            #self.response.write(template.render(template_values))
##            self.write(template_values)
##
##        else:
##            q=Quotes(quote=quote, author=author)
##            q.put()
##            self.redirect("/admin")

    def post(self):
        acct= self.request.get("quote")
        location= self.request.get("author")
        if acct==None or acct=="--quote--" or location==None or location=="--author--":
            error="Sorry must insert Values"
            template_values = {
            "quote":acct,
            "author":location,
            "error":error}
            #template = jinja_environment.get_template('admin.html')
            #self.response.write(template.render(template_values))
            self.write(template_values)

        else:
            q=Location(acct=acct, location=location)
            q.put()
            self.redirect("/admin")

            

class MainHandler(webapp2.RequestHandler):
    def write(self, values):
        template = jinja_environment.get_template('thoth.html')
        self.response.write(template.render(values))

    
    def get(self):
        template_values = {"contents":"", "all_selected":None,
                           "artificial_selected":None, "graphics_selected": None,
                           "programming_selected": None, "networking_selected": None,
                           "algorithms_selected": None, "databases_selected": None,
                           "no_contents":""}

        sort=None
        sort=self.request.get("sortdropdown")
        self.p= re.findall("(\.json?.*)$", self.request.url)
        
        if not sort or sort == "all":
            contents =db.GqlQuery("SELECT * FROM Content ORDER BY datetime DESC")
            all_selected= 'selected= "selected"'
            template_values["contents"]=contents
            template_values["all_selected"]=all_selected
            
            if any(self.p):
                contents =db.GqlQuery("SELECT * FROM Location")
                self.print_json(contents)
            else:
                self.write(template_values)



        else:
            contents =db.GqlQuery("SELECT * FROM Content WHERE %s_tag='True' ORDER BY datetime DESC" %(sort))
            template_values["contents"]=contents
            template_values["%s_selected" %sort]= 'selected= "selected"'
            if len(list(contents))<1:
                template_values["contents"]=""
                template_values["no_contents"]="No Content is available Under this Criteria"
                
            if any(self.p):
                contents =db.GqlQuery("SELECT * FROM Location")
                self.print_json(contents)
            else:
                self.write(template_values)


##    def print_json(self, contents):
##        self.dic={}
##        for a,b in enumerate(contents):
##            self.dic[a]={"Title":contents[a].heading, "Date":str(contents[a].datetime), "Link":"/contents?link=%s" %contents[a].link}
##        self.json_txt= json.dumps(self.dic)
##        self.response.headers["Content-Type"]="application/json; charset=utf-8"
##        self.response.write(self.json_txt)

    def print_json(self, contents):
        self.dic={}
        for a,b in enumerate(contents):
            self.dic[contents[a].acct]=contents[a].location
        

        #else: self.dic={"1": contents}
        self.json_txt= json.dumps(self.dic)
        self.response.headers["Content-Type"]="application/json; charset=utf-8"
        self.response.write(self.json_txt)
        
           
        """
        elif sort=="artificial":
            contents =db.GqlQuery("SELECT * from Content where artificial_tag='True' ORDER by datetime desc")
            artificial_selected= 'selected= "selected"'
            template_values["contents"]=contents
            template_values["artificial_selected"]=artificial_selected
            if len(list(contents))<1:
                template_values["contents"]=""
                template_values["no_contents"]="No Content is available Under this Criteria"
            self.write(template_values)
                


        elif sort=="programming":
            contents =db.GqlQuery("SELECT * from Content where programming_tag='True'")
            programming_selected= 'selected= "selected"'
            template_values["contents"]=contents
            template_values["programming_selected"]=programming_selected
            if len(list(contents))<1:
                template_values["contents"]=""
                template_values["no_contents"]="No Content is available Under this Criteria"
            self.write(template_values)
            

        elif sort=="graphics":
            contents =db.GqlQuery("SELECT * from Content where graphics_tag='True' ORDER by datetime desc")
            graphics_selected= 'selected= "selected"'
            template_values["contents"]=contents
            template_values["graphics_selected"]=graphics_selected
            if len(list(contents))<1:
                template_values["contents"]=""
                template_values["no_contents"]="No Content is available Under this Criteria"
            self.write(template_values)


        elif sort=="networking":
            contents =db.GqlQuery("SELECT * from Content where networking_tag='True' ORDER by datetime desc")
            networking_selected= 'selected= "selected"'
            template_values["contents"]=contents
            template_values["networking_selected"]=networking_selected
            if len(list(contents))<1:
                template_values["contents"]=""
                template_values["no_contents"]="No Content is available Under this Criteria"
            self.write(template_values)



        elif sort=="algorithms":
            contents =db.GqlQuery("SELECT * from Content where algorithms_tag='True' ORDER by datetime desc")
            algorithms_selected= 'selected= "selected"'
            template_values["contents"]=contents
            template_values["algorithms_selected"]=algorithms_selected
            if len(list(contents))<1:
                template_values["contents"]=""
                template_values["no_contents"]="No Content is available Under this Criteria"
            self.write(template_values)

        

        elif sort=="databases":
            contents =db.GqlQuery("SELECT * from Content where databases_tag='True' ORDER by datetime desc")
            databases_selected= 'selected= "selected"'
            template_values["contents"]=contents
            template_values["databases_selected"]=databases_selected
            if len(list(contents))<1:
                template_values["contents"]=""
                template_values["no_contents"]="No Content is available Under this Criteria"
            self.write(template_values)
                                        """

        
        
            

        

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


class AdminFrontHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = jinja_environment.get_template('adminfront.html')
        self.response.write(template.render())

    def post(self):
        name=self.request.get("name")
        pic=self.request.get("fileUpload")

        one_pic= Image(name=name, stored_image=pic)
        one_pic.put()

        #self.response.write("<html><title>Try</title><body><img src=pic></body><html>")

        #d=open("somename.jpg","wb")
        #d.write(pic)
        #d.close()
        self.response.write("<html><title>Try</title><body>this is the image u submited<br><img src='/image?img_id=%s'></body></html>" %name)
        #self.redirect("/image?img_id=%s" %name)

        
app = webapp2.WSGIApplication([
    ('/?(?:\.json)?', MainHandler),('/about', AboutHandler),
    ('/quotes', QuoteHandler),('/books', BookHandler),
    ('/portfolio', PortfolioHandler),('/education', EducationHandler),
    ('/downloads', DownloadHandler), ('/admin', AdminHandler),
    ('/adminfront', AdminFrontHandler), ('/image', ImageHandler),
    ('/admincontent', AdminContentHandler),('/contents', ContentHandler)
], debug=True)
