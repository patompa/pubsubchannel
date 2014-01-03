#!/usr/bin/env python
#
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.api import channel
from google.appengine.api import taskqueue
from google.appengine.api import namespace_manager
import json

class PullHandler(webapp.RequestHandler):
    def get(self):
        clientid = self.request.get('client')
       
        try:
          ns = self.request.get('namespace')
          if ns != "":
            namespace_manager.set(ns)
          q = taskqueue.Queue('pull-queue')
          tasks = q.lease_tasks_by_tag(100000,100,tag=clientid,deadline=30)
          result = []
          for task in tasks:
            result.append(json.loads(task.payload))
            q.delete_tasks(task)
   
          self.response.headers['Content-Type'] = 'application/json'   
          if self.request.get('callback') != '':
             self.response.write(self.request.get('callback') + "(" + json.dumps({"messages":result}) + ")");
          else:
             json.dump({"messages":result},self.response.out)
        except Exception, inst:
            self.response.write(inst)
            
app = webapp.WSGIApplication([('/pull', PullHandler)],
                                         debug=True)

