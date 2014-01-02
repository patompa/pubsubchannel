#!/usr/bin/env python
#
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.api import channel
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
        tokens = memcache.get(group)
        try:
          body = self.request.body
          for token in tokens:
            if token != intoken:
                message = json.loads(body);
                channel.send_message(token,json.dumps(message))
        except Exception, inst:
            self.response.write(inst)
            self.response.write(" " + body)
            
            
app = webapp.WSGIApplication([('/publish', PublishHandler)],
                                         debug=True)

