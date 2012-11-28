#!/usr/bin/env python
#
# This is an sample AppEngine application that shows how to 1) log in a user
# using the LinkedIn OAuth API and 2) extract their profile.
#
# INSTRUCTIONS:
#
# 1. Set up a new AppEngine application using this file, let's say on port
# 8080. Rename this file to main.py, or alternatively modify your app.yaml
# file.)
# 2. Fill in the application ("consumer") key and secret lines below.
# 3. Visit http://localhost:8080 and click the "login" link to be redirected
# to LinkedIn.com.
# 4. Once verified, you'll be redirected back to your app on localhost and
# you'll see some of your Twitter user info printed in the browser.
# 5. Copy and paste the token and secret info into this file, replacing the
# default values for user_token and user_secret. You'll need the user's token
# & secret info to interact with the Twitter API on their behalf from now on.
# 6. Finally, visit http://localhost:8080/timeline to see your twitter
# timeline.
#

__author__ = "Mike Knapp, Kirsten Jones"

import oauth

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import taskqueue
from google.appengine.ext import db
from google.appengine.api import memcache

import logging
import networkx as nx
import json
import urllib
import graphAnalys as ga

class MainHandler(webapp.RequestHandler):
  def get(self, mode=""):  
      application_key = "xm193vpcuad6"
      application_secret = "9FVc1SQLVnvBbJpo"

      user_token = ""
      user_secret = ""
      # In the real world, you'd want to edit this callback URL to point to your
      # production server. This is where the user is sent to after they have
      # authenticated with Twitter.
      callback_url = "%s/verify" % self.request.host_url

      client = oauth.LinkedInClient(application_key, application_secret, callback_url)

      if mode == "login":
        return self.redirect(client.get_authorization_url())

      if mode == "verify":
        auth_token = self.request.get("oauth_token")
        auth_verifier = self.request.get("oauth_verifier")
        auth_token_secret = self.request.get("oauth_token_secret")
        user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)
        
        url = "http://api.linkedin.com/v1/people/~:(skills)"
        connectionurl = "http://api.linkedin.com/v1/people/~/connections"

        user_token = user_info['token']
        user_secret = user_info['secret']
        user_name = user_info['name']
        data = client.make_request(url, token = user_token, secret = user_secret, additional_params={"format":"json"})

        g = nx.DiGraph()
        firstDegreeConnectionsId = {}

        data = client.make_request(connectionurl, token = user_token, secret = user_secret, additional_params={"format":"json"})
        dictionary = json.loads(data.content)
        firstDegreeConnections = []
        for v in dictionary['values']:
          s = v['firstName']
          s = s.encode('ascii', 'ignore')
          b = v['lastName']
          b = b.encode('ascii', 'ignore')
          ba = s + " " + b
          c = v['id']
          c = c.encode('ascii', 'ignore')
          firstDegreeConnectionsId[c] = ba
          firstDegreeConnections.append(ba)
        for i in firstDegreeConnections:
          me = user_name
          g.add_edge(me.encode("latin-1"), i.encode("latin-1"))


        for k, v in firstDegreeConnectionsId.iteritems():
            testurl = "http://api.linkedin.com/v1/people/id=%s:(relation-to-viewer:(related-connections))" % k
            data = client.make_request(testurl, token = user_token, secret = user_secret, additional_params={"format":"json" })
            jsondict = json.loads(data.content)
            try:
                for element in jsondict['relationToViewer']['relatedConnections']['values']:
                    s = element['firstName']
                    s = s.encode('ascii', 'ignore')
                    b = element['lastName']
                    b = b.encode('ascii', 'ignore')
                    ba = s + " " + b
                    g.add_edge(v.encode("latin-1"), ba.encode("latin-1"))
            except KeyError:
                print "ble" 
        
        url = "http://api.linkedin.com/v1/people/~:(skills)"
        data = client.make_request(url, token = user_token, secret = user_secret, additional_params={"format":"json" })
        logging.info(data)
        dictionary = json.loads(data.content)
        listOfSkills = []
        for value in dictionary['skills']['values']:
          for key, skill in value['skill'].iteritems():
            listOfSkills.append(skill)

        secondDegreeRelationIdsWithSkillSearchDict = {}

        listOfSkills = listOfSkills[:4]

        for i in listOfSkills:
          i = urllib.quote_plus(i)
          url = "http://api.linkedin.com/v1/people-search:(people:(relation-to-viewer,id,first-name,last-name,location:(name,country:(code),postal-code),connections))"
          data = client.make_request(url, token = user_token, secret = user_secret, additional_params={"facets":"network", "facet":"network,S", "format":"json", "start" :"0", "count" : "25", "keywords" : "%s" % i})
          jsondict = json.loads(data.content)
          for k, b in jsondict['people'].iteritems():
            if k == 'values':
              for v in b:
                s = v['firstName']
                s = s.encode('ascii', 'ignore')
                b = v['lastName']
                b = b.encode('ascii', 'ignore')
                ba = s + " " + b
                c = v['id']
                c = c.encode('ascii', 'ignore')
                secondDegreeRelationIdsWithSkillSearchDict[c] = ba
        # for i in listOfSkills:
        #   i = urllib.quote_plus(i)
        #   url = "http://api.linkedin.com/v1/people-search:(people:(relation-to-viewer,id,first-name,last-name,location:(name,country:(code),postal-code),connections))"
        #   data = client.make_request(url, token = user_token, secret = user_secret, additional_params={"facets":"network", "facet":"network,S", "format":"json", "start" :"25", "count" : "25", "keywords" : "%s" % i})
        #   jsondict = json.loads(data.content)
        #   for k, b in jsondict['people'].iteritems():
        #     if k == 'values':
        #       for v in b:
        #         s = v['firstName']
        #         s = s.encode('ascii', 'ignore')
        #         b = v['lastName']
        #         b = b.encode('ascii', 'ignore')
        #         ba = s + " " + b
        #         c = v['id']
        #         c = c.encode('ascii', 'ignore')
        #         secondDegreeRelationIdsWithSkillSearchDict[c] = ba
        # for i in listOfSkills:
        #   i = urllib.quote_plus(i)
        #   url = "http://api.linkedin.com/v1/people-search:(people:(relation-to-viewer,id,first-name,last-name,location:(name,country:(code),postal-code),connections))"
        #   data = client.make_request(url, token = user_token, secret = user_secret, additional_params={"facets":"network", "facet":"network,S", "format":"json", "start" :"50", "count" : "25", "keywords" : "%s" % i})
        #   jsondict = json.loads(data.content)
        #   for k, b in jsondict['people'].iteritems():
        #     if k == 'values':
        #       for v in b:
        #         s = v['firstName']
        #         s = s.encode('ascii', 'ignore')
        #         b = v['lastName']
        #         b = b.encode('ascii', 'ignore')
        #         ba = s + " " + b
        #         c = v['id']
        #         c = c.encode('ascii', 'ignore')
        #         secondDegreeRelationIdsWithSkillSearchDict[c] = ba
        # for i in listOfSkills:
        #   i = urllib.quote_plus(i)
        #   url = "http://api.linkedin.com/v1/people-search:(people:(relation-to-viewer,id,first-name,last-name,location:(name,country:(code),postal-code),connections))"
        #   data = client.make_request(url, token = user_token, secret = user_secret, additional_params={"facets":"network", "facet":"network,S", "format":"json", "start" :"50", "count" : "25", "keywords" : "%s" % i})
        #   jsondict = json.loads(data.content)
        #   for k, b in jsondict['people'].iteritems():
        #     if k == 'values':
        #       for v in b:
        #         s = v['firstName']
        #         s = s.encode('ascii', 'ignore')
        #         b = v['lastName']
        #         b = b.encode('ascii', 'ignore')
        #         ba = s + " " + b
        #         c = v['id']
        #         c = c.encode('ascii', 'ignore')
        #         secondDegreeRelationIdsWithSkillSearchDict[c] = ba
        for k, v in secondDegreeRelationIdsWithSkillSearchDict.iteritems():
          url = "http://api.linkedin.com/v1/people/id=%s:(relation-to-viewer:(related-connections))" % k
          data = client.make_request(url, token = user_token, secret = user_secret, additional_params={"format":"json"})
          jsondict = json.loads(data.content)
          try:
            for element in jsondict['relationToViewer']['relatedConnections']['values']:
              s = element['firstName']
              s = s.encode('ascii', 'ignore')
              b = element['lastName']
              b = b.encode('ascii', 'ignore')
              ba = s + " " + b
              g.add_edge(v.encode("latin-1"), ba.encode("latin-1"))
          except KeyError:
            print "ble"
            
        outP = ga.DrawGraph(g, user_name)
        self.response.out.write(outP)


      if mode == "linkedin":
        profile_url = "http://api.linkedin.com/v1/people/~"
        
        result = client.make_request(url=profile_url,token=user_token,secret=user_secret)
        self.response.out.write("<a href='/'>start over</a><br /><br />")
        return self.response.out.write(result.content)

      self.response.out.write("<a href='/login'>login with linkedin</a>")


app = webapp.WSGIApplication([('/(.*)', MainHandler)], debug=True)
