#!/usr/bin/env python
#
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.api import channel
from google.appengine.api import taskqueue
from google.appengine.api import namespace_manager
import json

class PublishHandler(webapp.RequestHandler):
    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Method'] = 'OPTIONS,POST'
        self.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        self.response.headers['Access-Control-Allow-Content-Type'] = 'application/json'
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
                message = json.loads(body);
                if token.startswith("PULL_"):
                    q = taskqueue.Queue('pull-queue')
                    tasks = []
                    payload_str = json.dumps(message)
                    tasks.append(taskqueue.Task(payload=payload_str, method='PULL',tag=token))
                    q.add(tasks)
                else:
                    channel.send_message(token,json.dumps(message))
        except Exception, inst:
            self.response.write(inst)
            self.response.write(" " + body)
            
            
app = webapp.WSGIApplication([('/publish', PublishHandler)],
                                         debug=True)

