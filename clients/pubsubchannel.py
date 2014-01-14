#! /usr/bin/env python
import requests
import uuid
import json
import threading

class pubsubchannel(object):
  def __init__(self,server="http://pubsubchannel.appspot.com/",namespace="",logfile=""):
    self.SERVER = server
    self.client = "PULL_" + str(uuid.uuid4()).replace('-','') 
    self.token = ""
    self.threads = []
    self.groups = []
    self.namespace=namespace
    self.logfile=logfile

  def getNS(self):
    if self.namespace == "":
        return ""
    return "&namespace=" + self.namespace
 
  def publish(self,group,message) :
   url = self.SERVER + 'publish?group=' + group + '&token=' + self.token + self.getNS()
   r = requests.post(url,data=json.dumps(message), headers={'Content-Type':'application/json'})

  def subscribe(self,group):
   url = self.SERVER + 'subscribe?group=' + group + '&client=' + self.client + self.getNS()
   r = requests.get(url)
   self.token = json.loads(r.text)['token']
   self.groups.append(group)

  def listen(self,callback=None):
   thread = PollThread(self.client,self.SERVER,self.namespace,self.groups,self.logfile,callback)
   thread.start()
   self.threads.append(thread)

  def stop(self):
     for thread in self.threads:
       thread.stopped = True
       thread.join()

class PollThread(threading.Thread):
  def __init__(self,client,SERVER,namespace,groups,logfile,callback):
      threading.Thread.__init__(self)
      self.client = client    
      self.callback = callback
      self.stopped = False
      self.SERVER = SERVER
      self.namespace = namespace
      self.groups = groups
      self.logfile = logfile

  def resubscribe(self,group):
   url = self.SERVER + 'subscribe?group=' + group + '&client=' + self.client + self.getNS()
   r = requests.get(url)

  def getNS(self):
    if self.namespace == "":
        return ""
    return "&namespace=" + self.namespace

  def logError(self,message, error):
      import time
      if self.logfile == "":
          return
      f = open(self.logfile,'a')
      f.write("[%.2f] %s: %s %s\n" % (time.time(),message,type(error).__name__,error)) 
      f.close()

  def run(self):
   import time
   lastsubscribe = time.time()
   while not self.stopped:
     url = self.SERVER + 'pull?client=' + self.client + self.getNS()
     r = requests.get(url)
     try:
       messages = json.loads(r.text)['messages']
     except Exception, inst:
         self.logError("JSON Error",inst)
     for msg in messages:
       if self.callback is not None:
           try:
             self.callback(msg)
           except Exception, inst:
             self.logError("Callback Error",inst)
       else:
           print msg
     if time.time() - lastsubscribe > 60:
         lastsubscribe = time.time()
         for group in self.groups:
             self.resubscribe(group) 

if __name__ == '__main__':
    import sys
    USAGE = "Usage: pubsubchannel <publish>|<subscribe> <group> (<message>)"
    if len(sys.argv) < 3 :
       print USAGE
       sys.exit(1)
    action = sys.argv[1]
    group = sys.argv[2]
    if action == "subscribe":
        if len(sys.argv) != 3:
            print USAGE
            sys.exit(1) 
        channel = pubsubchannel()
        channel.subscribe(group)
        channel.listen()
        print "Press Enter to exit."
        sys.stdin.read(1)
        print "Exiting...."
        channel.stop()
        sys.exit(0)
    elif action == "publish":
        if len(sys.argv) != 4:
            print USAGE
            sys.exit(1) 
        message = json.loads(sys.argv[3])
        channel = pubsubchannel()
        channel.publish(group,message) 
