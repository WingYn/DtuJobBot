import oauth2 as oauth
import httplib2
import time, os, simplejson
 
# Fill the keys and secrets you retrieved after registering your app
api_key      =   'zt33uu6fiiw8'
secret_key  =   '5e7rUflDxDLhXPYh'
user_token           =   '134d9126-f72a-48fa-81de-69e160dd4466'
user_secret          =   'a4a0f762-1ee6-46c7-a3de-96e522d6e4a7'
 
# Use your API key and secret to instantiate consumer object
consumer = oauth.Consumer(api_key, secret_key)
 
# Use your developer token and secret to instantiate access token object
access_token = oauth.Token(
            key=user_token,
            secret=user_secret)
 
client = oauth.Client(consumer, access_token)
 
# Make call to LinkedIn to retrieve your own profile
resp,content = client.request("http://api.linkedin.com/v1/people/~", "GET", {})

# By default, the LinkedIn API responses are in XML format. If you prefer JSON, simply specify the format in your call
# resp,content = client.request(""http://api.linkedin.com/v1/people/~?format=json", "GET", {})
