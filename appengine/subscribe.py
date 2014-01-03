#!/usr/bin/env python
#
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.api import channel
from google.appengine.api import namespace_manager
import json


class SubscribeHandler(webapp.RequestHandler):
    def get(self):
        clientid = self.request.get('client')
        group = self.request.get('group')
        ns = self.request.get('namespace')
        if ns != "":
            namespace_manager.set(ns)

        if clientid.startswith("PULL_"):
            token = clientid
        else:
            token = channel.create_channel(clientid)

        tokens = memcache.get(group)
        if tokens is None:
            tokens = []

        if not token in tokens:
            tokens.append(token)
            memcache.set(group,tokens,60*60*24)
   
        self.response.headers['Content-Type'] = 'application/json'   
        if self.request.get('callback') != '':
           self.response.write(self.request.get('callback') + "(" + json.dumps({"token":token}) + ")");
        else:
           json.dump({"token":token},self.response.out)
            
            

app = webapp.WSGIApplication([('/subscribe', SubscribeHandler)],
                                         debug=True)

