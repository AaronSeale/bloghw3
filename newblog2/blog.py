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
  blog_title = db.StringProperty(required = True)
  blog_entry = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)
  
#!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Delete MainPage<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!#

"""class Delete(baseHandler):
  
  def get(self, subject="", content="", error=""):
    db_blog = db.GqlQuery("SELECT * FROM Eric ORDER BY created DESC")
    db.delete(Eric.all())
    self.render("delete.html", subject=subject, content=content, db_blog=db_blog)"""
    
      

#!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Blog MainPage<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!#  
class Blog(baseHandler):
  
  def get(self, blog_title="", blog_entry=""):
    db_blog = db.GqlQuery("SELECT * FROM Eric ORDER BY created DESC")
    self.render("blog.html", db_blog=db_blog)
    
  
  
    
#!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>New Post<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!#      
class NewPost(baseHandler):
  
  def render_newpost(self, blog_title="", blog_entry="", error=""):
    self.render("newpost.html", blog_title=blog_title, blog_entry=blog_entry, error=error)
    
  def get(self):
    self.render_newpost()
    
  def post(self):
    blog_title = self.request.get("subject")
    blog_entry = self.request.get("content")
    
    if blog_title and blog_entry:
      p = Eric(blog_title=blog_title, blog_entry=blog_entry)
      p.put()
    
    
      self.redirect('/blog')
      
    else:
      error = "We need text in both the Subject & Content boxes please"
      #self.render("newpost.html", error = error)
      self.render_newpost(blog_title, blog_entry, error)
         

#!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Page Mapping<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!#

app = webapp2.WSGIApplication([('/blog', Blog), ('/blog/newpost', NewPost)], debug=True)
                               #('/blog', Blog)],