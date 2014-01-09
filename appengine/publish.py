#!/usr/bin/env python
#
from google.appengine.ext import webapp
from google.appengine.api import memcache
#from google.appengine.api import channel
from google.appengine.api import taskqueue
from google.appengine.api import namespace_manager
import json

class PublishHandler(webapp.RequestHandler):
    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Method'] = 'OPTIONS,POST'
        self.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        self.response.headers['Access-Control-Allow-Content-Type'] = 'application/json'

    def removeClient(self,token,group):
      client = memcache.Client()
      retries = 0
      MAX_RETRIES = 10
      while retries < MAX_RETRIES:
        retries += 1
        tokens = client.gets(group)
        if tokens is None:
          tokens = []
	  client.set(group,[])
	  continue;
        if token in tokens:
          tokens.remove(token)
	  if client.cas(group,tokens,60*60*24*2):
            return True
        else:
          return True
      return False

    def addMessage(self,token,message,group):
	 import time
	 client = memcache.Client()
	 retries = 0
         MAX_RETRIES = 100
         while retries < MAX_RETRIES:
	   retries += 1
           messages = client.gets(token)
	   if messages is None:
	     client.set(token,[])
	     continue
           else:
	     messages.append({'message':message,'time':time.time()})
	   if client.cas(token,messages,60*60*24):
	     if len(messages) > 200:
	         self.removeClient(token,group)
             return True
         return False

    def post(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Method'] = 'POST'
        self.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        self.response.headers['Access-Control-Allow-Content-Type'] = 'application/json'
        group = self.request.get('group')
        intoken = self.request.get('token')
        ns = self.request.get('namespace')
        if ns != "":
            namespace_manager.set(ns)
            
        tokens = memcache.get(group)
        try:
          body = self.request.body
          for token in tokens:
            if token != intoken:
                #message = json.loads(body);
                #if token.startswith("PULL_"):
                self.addMessage(token,body,group)
		# task queues may be used here but they tend to eat up quota
		#
                #q = taskqueue.Queue('pull-queue')
                #tasks = []
                #payload_str = json.dumps(message)
                #tasks.append(taskqueue.Task(payload=payload_str, method='PULL',tag=token))
                #q.add(tasks)
                #else:
                #    channel.send_message(token,json.dumps(message))
        except Exception, inst:
            self.response.write(inst)
            self.response.write(" " + body)
            
            
app = webapp.WSGIApplication([('/publish', PublishHandler)],
                                         debug=True)

