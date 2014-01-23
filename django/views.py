#! /usr/bin/env python
from django.http import HttpResponse
from json import dumps, loads
from django.conf import settings
import memcache


def addClient(token,group):
  client = memcache.Client(settings.CAS_HOSTS)
  retries = 0
  while retries < settings.CAS_MAX_SUBSCRIBE_RETRIES:
        retries += 1
        tokens = client.gets(group)
        if tokens is None:
          client.set(group,[])
          continue
        if not token in tokens:
          tokens.append(token)
          if client.cas(group,tokens,time=settings.CAS_TTL):
            return True
        else:
          return True
  return False

def getMessages(clientid):
  client = memcache.Client(settings.CAS_HOSTS)
  retries = 0
  messages = []
  while retries < settings.CAS_MAX_MESSAGE_RETRIES:
    retries += 1
    messages = client.gets(clientid)
    if messages is None:
      client.set(clientid,[])
      continue
    if client.cas(clientid,[]):
      break
  return messages

def removeClient(token,group):
  client = memcache.Client(settings.CAS_HOSTS)
  retries = 0
  while retries < CAS_MAX_REMOVE_RETRIES:
    retries += 1
    tokens = client.gets(group)
    if tokens is None:
      tokens = []
      client.set(group,[])
      continue;
    if token in tokens:
      tokens.remove(token)
      if client.cas(group,tokens,settings.CAS_TTL):
        return True
    else:
        return True
  return False

def addMessage(token,message,group):
  import time
  client = memcache.Client(settings.CAS_HOSTS)
  retries = 0
  while retries < settings.CAS_MAX_MESSAGE_RETRIES:
    retries += 1
    messages = client.gets(token)
    if messages is None:
      client.set(token,[])
      continue
    else:
      messages.append({'message':message,'time':time.time()})
      if client.cas(token,messages,settings.CAS_TTL):
        if len(messages) > 200:
          removeClient(token,group)
        return True
  return False

def addHeaders(response):
   response['Access-Control-Allow-Origin'] = '*'
   response['Access-Control-Allow-Method'] = 'OPTIONS,POST,GET'
   response['Access-Control-Allow-Headers'] = 'Content-Type'
   response['Access-Control-Allow-Content-Type'] = 'application/json'
   return response

def toResponse(result):
  return addHeaders(HttpResponse(dumps(result)))

def subscribe(request):
   clientid = str(request.GET['client'])
   group = str(request.GET['group'])
   token = clientid
   if not addClient(token,group):
     token = ""
   return toResponse({'token':token})

def pull(request):
   import time
   clientid = str(request.GET['client'])
   tries = 0
   result = []
   while tries < settings.MAX_PULL_RETRIES:
     messages = getMessages(clientid)
     result = []
     if messages is not None:
       for message in messages:
         result.append(loads(message['message']))
     if len(result) == 0:
       tries += 1
       time.sleep(1)
     else:
       break
   return toResponse({'messages':result})

def publish(request):
  group = str(request.GET['group'])
  intoken = str(request.GET['token'])

  client = memcache.Client(settings.CAS_HOSTS)
  tokens = client.get(group)
  try:
    body = request.raw_post_data
    for token in tokens:
      if token != intoken:
        addMessage(token,body,group)
  except Exception, inst:
    return toResponse({'error':"%s" % inst})
  return toResponse({}) 
