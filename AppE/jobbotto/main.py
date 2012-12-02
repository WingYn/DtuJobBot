import webapp2
from google.appengine.ext.webapp import util
import jinja2
import os
import graphAnalys as ga
import networkx as nx
import link_clustering as lc
import logging

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self): 
        # Title
        self.response.out.write("<p>DTU Job Bot</p>")

        # Classification

        self.response.out.write("""<center><a STYLE="position:absolute; TOP:10px; LEFT:800px; WIDTH:50px; HEIGHT:50px" href='/classification'>Classification</a><center>""") 

        # About

        self.response.out.write("""<center><a STYLE="position:absolute; TOP:10px; LEFT:900px; WIDTH:50px; HEIGHT:50px" href='/about'>About</a><center>""") 

        # Generate Graph
        self.response.out.write("<br /><br /><br /><br /><br /><br /><center><a href='/generategraph/login'>Generate your own LinkedIn network</a><center>") 
        self.response.out.write("<center>")
        # self.response.out.write(ga.DrawGraph(nx.read_graphml('newGraph.xml'), 'Sin'))
        self.response.out.write("<center>")

        # logging.info(lc.main('bla'))

app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
