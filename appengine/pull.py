#!/usr/bin/env python
#
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.api import taskqueue
from google.appengine.api import namespace_manager
import json

class PullHandler(webapp.RequestHandler):
    
    def options(self):
      self.response.headers['Access-Control-Allow-Origin'] = '*'
      self.response.headers['Access-Control-Allow-Method'] = 'OPTIONS,POST,GET'
      self.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
      self.response.headers['Access-Control-Allow-Content-Type'] = 'application/json'


    def getMessages(self,clientid):
      client = memcache.Client()
      retries = 0
      MAX_RETRIES = 100
      messages = []
      while retries < MAX_RETRIES:
	retries += 1
        messages = client.gets(clientid)
	if messages is None:
	  client.set(clientid,[])
	  continue
	if client.cas(clientid,[]):
	  break
      return messages
	        
    def get(self):
	self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Method'] = 'OPTIONS,POST,GET'
        self.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        self.response.headers['Access-Control-Allow-Content-Type'] = 'application/json'
	import time
        clientid = self.request.get('client')

       
        try:
          ns = self.request.get('namespace')
          if ns != "":
            namespace_manager.set(ns)
	  # task queues may be used here but they tend to eat up quota
	  #
          #q = taskqueue.Queue('pull-queue')
          #tasks = q.lease_tasks_by_tag(100000,100,tag=clientid,deadline=30)
          #result = []
          #for task in tasks:
          #  result.append(json.loads(task.payload))
          #  q.delete_tasks(task)
	  MAX_TRIES = 30
	  tries = 0
	  result = []
	  while tries < MAX_TRIES:
	    messages = self.getMessages(clientid)
	    result = []
	    if messages is not None:
	      for message in messages:
		result.append(json.loads(message['message']))
	    if len(result) == 0:
              tries += 1
	      time.sleep(1)
	    else:
	      break
   
          self.response.headers['Content-Type'] = 'application/json'   
          if self.request.get('callback') != '':
             self.response.write(self.request.get('callback') + "(" + json.dumps({"messages":result}) + ")");
          else:
             json.dump({"messages":result},self.response.out)
        except Exception, inst:
            self.response.write(inst)
            
app = webapp.WSGIApplication([('/pull', PullHandler)],
                                         debug=True)

