#!/usr/bin/env python
#
from google.appengine.ext import webapp
from google.appengine.api import memcache
#from google.appengine.api import channel
from google.appengine.api import namespace_manager
import json


class SubscribeHandler(webapp.RequestHandler):
    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Method'] = 'OPTIONS,POST,GET'
        self.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        self.response.headers['Access-Control-Allow-Content-Type'] = 'application/json'

    def addClient(self,token,group):
      client = memcache.Client()
      retries = 0
      MAX_RETRIES = 1000
      while retries < MAX_RETRIES:
	retries += 1
        tokens = client.gets(group)
        if tokens is None:
          client.set(group,[])
          continue
        if not token in tokens:
          tokens.append(token)
	  if client.cas(group,tokens,time=60*60*24*2):
            return True
        else:
          return True
      return False

    def post(self):
        self.get()

    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Method'] = 'OPTIONS,POST,GET'
        self.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        self.response.headers['Access-Control-Allow-Content-Type'] = 'application/json'
        clientid = self.request.get('client')
        group = self.request.get('group')
        ns = self.request.get('namespace')
        if ns != "":
            namespace_manager.set(ns)

        #if clientid.startswith("PULL_"):
        token = clientid
        #else:
        #    token = channel.create_channel(clientid)

	if not self.addClient(token,group):
	  token = ""
   
        self.response.headers['Content-Type'] = 'application/json'   
        if self.request.get('callback') != '':
           self.response.write(self.request.get('callback') + "(" + json.dumps({"token":token}) + ")");
        else:
           json.dump({"token":token},self.response.out)
            
            

app = webapp.WSGIApplication([('/subscribe', SubscribeHandler)],
                                         debug=True)

