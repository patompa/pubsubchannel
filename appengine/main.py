#!/usr/bin/env python
#
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class MainHandler(webapp.RequestHandler):
    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Method'] = 'OPTIONS,POST,GET'
        self.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        self.response.headers['Access-Control-Allow-Content-Type'] = 'application/json'
    def get(self):
	self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Method'] = 'OPTIONS,POST,GET'
        self.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        self.response.headers['Access-Control-Allow-Content-Type'] = 'application/json'
        path = os.path.join(os.path.dirname(__file__),'pubsub.js')
        self.response.out.write(template.render(path, {}))
      


app = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)

