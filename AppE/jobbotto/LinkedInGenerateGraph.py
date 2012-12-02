import webapp2
import oauth

import logging
import networkx as nx
import json
import urllib
import graphAnalys as ga

class GraphGenerationHandler(webapp2.RequestHandler):
	def get(self, mode = ""):
		application_key = "xm193vpcuad6"
		application_secret = "9FVc1SQLVnvBbJpo"

		user_token = ""
		user_secret = ""
		callback_url = "%s/generategraph/verify" % self.request.host_url

		client = oauth.LinkedInClient(application_key, application_secret, callback_url)
		
		if mode == 'login':
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
			# data = client.make_request(url, token = user_token, secret = user_secret, additional_params={"format":"json"})

			g = nx.DiGraph()
			firstDegreeConnectionsId = {}

			data = client.make_async_request(connectionurl, token = user_token, secret = user_secret, additional_params={"format":"json"})
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
			    data = client.make_async_request(testurl, token = user_token, secret = user_secret, additional_params={"format":"json" })
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
			data = client.make_async_request(url, token = user_token, secret = user_secret, additional_params={"format":"json" })
			logging.info(data)
			dictionary = json.loads(data.content)
			listOfSkills = []
			for value in dictionary['skills']['values']:
			  for key, skill in value['skill'].iteritems():
			    listOfSkills.append(skill)

			secondDegreeRelationIdsWithSkillSearchDict = {}

			listOfSkills = listOfSkills[:5]

		for i in listOfSkills:
			i = urllib.quote_plus(i)
			url = "http://api.linkedin.com/v1/people-search:(people:(relation-to-viewer,id,first-name,last-name,location:(name,country:(code),postal-code),connections))"
			data = client.make_async_request(url, token = user_token, secret = user_secret, additional_params={"facets":"network", "facet":"network,S", "format":"json", "start" :"0", "count" : "25", "keywords" : "%s" % i})
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
		for i in listOfSkills:
			i = urllib.quote_plus(i)
			url = "http://api.linkedin.com/v1/people-search:(people:(relation-to-viewer,id,first-name,last-name,location:(name,country:(code),postal-code),connections))"
			data = client.make_async_request(url, token = user_token, secret = user_secret, additional_params={"facets":"network", "facet":"network,S", "format":"json", "start" :"25", "count" : "25", "keywords" : "%s" % i})
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
		for i in listOfSkills:
			i = urllib.quote_plus(i)
			url = "http://api.linkedin.com/v1/people-search:(people:(relation-to-viewer,id,first-name,last-name,location:(name,country:(code),postal-code),connections))"
			data = client.make_async_request(url, token = user_token, secret = user_secret, additional_params={"facets":"network", "facet":"network,S", "format":"json", "start" :"50", "count" : "25", "keywords" : "%s" % i})
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
		for i in listOfSkills:
			i = urllib.quote_plus(i)
			url = "http://api.linkedin.com/v1/people-search:(people:(relation-to-viewer,id,first-name,last-name,location:(name,country:(code),postal-code),connections))"
			data = client.make_async_request(url, token = user_token, secret = user_secret, additional_params={"facets":"network", "facet":"network,S", "format":"json", "start" :"50", "count" : "25", "keywords" : "%s" % i})
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
		for k, v in secondDegreeRelationIdsWithSkillSearchDict.iteritems():
			url = "http://api.linkedin.com/v1/people/id=%s:(relation-to-viewer:(related-connections))" % k
			data = client.make_async_request(url, token = user_token, secret = user_secret, additional_params={"format":"json"})
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

app = webapp2.WSGIApplication([('/generategraph/(.*)', GraphGenerationHandler)], debug=True)






