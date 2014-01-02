#!/usr/bin/env python
#
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class MainHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__),'pubsub.js')
        self.response.out.write(template.render(path, {}))
      


app = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)

