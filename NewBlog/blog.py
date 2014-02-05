import os
import re 
import webapp2  
import jinja2 

from google.appengine.ext import db 

template_dir = os.path.join(os.path.dirname(__file__), 'templates') 
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True) 


#!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Basic Setup<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!#
class baseHandler(webapp2.RequestHandler): 
    
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)
    
  def render_str(self, template, **params): 
    t = jinja_env.get_template(template)    
    return t.render(params)
    
  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))
    
class Eric(db.Model):
  subject = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)
  
#!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Delete MainPage<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!#

class Delete(baseHandler):
  
  def get(self, subject="", content="", error=""):
    db_blog = db.GqlQuery("SELECT * FROM Eric ORDER BY created DESC")
    db.delete(Eric.all())
    self.render("delete.html", subject=subject, content=content, db_blog=db_blog)
    
      

#!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Blog MainPage<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!#  
class Blog(baseHandler):
  
  def get(self, subject="", content="", error=""):
    db_blog = db.GqlQuery("SELECT * FROM Eric ORDER BY created DESC")
    self.render("blog.html", subject=subject, content=content, db_blog=db_blog)
    
  
  
    
#!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>New Post<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!#      
class NewPost(baseHandler):
  
  def render_newpost(self, subject="", content="", error=""):
    self.render("newpost.html", subject=subject, content=content, error=error)
    
    
    
  def get(self):
    self.render_newpost()
    
  def post(self):
    subject = self.request.get("subject")
    content = self.request.get("content")
    
    if subject and content:
      #self.write("Added New Post!")
      p = Eric(subject=subject, content=content)
      p.put()
    
    
      self.redirect('/blog')
      
    else:
      error = "We need text in both the Subject & Content boxes please"
      #self.render("newpost.html", error = error)
      self.render_newpost(subject, content, error)
         

#!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Page Mapping<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!#

app = webapp2.WSGIApplication([('/blog', Blog), ('/blog/newpost', NewPost), ('/blog/delete', Delete)], debug=True)
                               #('/blog', Blog)],