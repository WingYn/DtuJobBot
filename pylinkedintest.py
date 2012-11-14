import oauth2 as oauth
import httplib2
import time, os, simplejson
 
# Fill the keys and secrets you retrieved after registering your app
api_key      =   'zt33uu6fiiw8'
secret_key  =   '5e7rUflDxDLhXPYh'
user_token           =   'd6085e21-fa8c-4eab-9cd4-8709053ddacf'
user_secret          =   '79d0247d-b2e5-46b9-9a36-2ab90bf6b65f'
 
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
