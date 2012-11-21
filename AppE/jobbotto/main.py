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

import logging

class MainHandler(webapp.RequestHandler):

  def get(self, mode=""):
    application_key = "zt33uu6fiiw8"
    application_secret = "5e7rUflDxDLhXPYh"

    # Fill in the next 2 lines after you have successfully logged in to
    # Twitter per the instructions above. This is the *user's* token and
    # secret. You need these values to call the API on their behalf after
    # they have logged in to your app.
    user_token = ""
    user_secret = ""
    
    # In the real world, you'd want to edit this callback URL to point to your
    # production server. This is where the user is sent to after they have
    # authenticated with Twitter.
    callback_url = "%s/verify" % self.request.host_url

    client = oauth.LinkedInClient(application_key, application_secret,
        callback_url)

    if mode == "login":
      return self.redirect(client.get_authorization_url())

    if mode == "verify":
      auth_token = self.request.get("oauth_token")
      auth_verifier = self.request.get("oauth_verifier")
      auth_token_secret = self.request.get("oauth_token_secret")
      user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)
      self.response.out.write("<br />oauth_token_secret"+auth_token_secret+"<br />oauth_token: "+auth_token+"<br />oauth_verifier: "+auth_verifier+"<br />")
      return self.response.out.write(user_info)

    if mode == "linkedin":
      profile_url = "http://api.linkedin.com/v1/people/~"
      
      result = client.make_request(url=profile_url,token=user_token,secret=user_secret)
      self.response.out.write("<a href='/'>start over</a><br /><br />")
      return self.response.out.write(result.content)

    self.response.out.write("<a href='/login'>login with linkedin</a>")



# def main():
app = webapp.WSGIApplication([('/(.*)', MainHandler)],
                                       debug=True)
  # util.run_wsgi_app(app)


# if __name__ == '__main__':
#   main()

# main()