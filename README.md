pubsubchannel
=============

A Hosted Multi-tenant Web and Native Publish-Subscribe Event Channel for Google App Engine.
The Event Channel utilizes the App Engine services Memcache (CAS), and Namespaces.
Task Queues and Channels were used in early versions but dropped because they
require more quota, and have no garbage collection control respectively.

Javascript Frontend
-------

Add:
```html
	<script type="text/javascript" src="http://pubsubchannel.appspot.com/"></script>
```

where pubsubchannel is the app id of your Google App Engine application where the 
channel is deployed.

To send messages call:

	PubSub.publish("demo",{'msg':"Hello world from " + PubSub.id()});

To receive messages call:

	PubSub.subscribe("demo",function (json) {console.log(json.msg)});

Google App Engine Backend
-------

In the app.yaml file change the APP_ID to your google app engine application id.
In the pubsub.js file change APP_ID to your google app engine application id.

A live demo deployment is avalable at pubsubchannel.appspot.com 

Native Python Client
-------
For non-browser clients there is a long-polling REST interface based on App Engine Task Queues.
The only thing the client needs to do is to call the pull REST API as exemplified by the
python client in the distribution. The example python client depends on the requests
and threading packages, but any http client library may be used.

To listen to events on the demo channel use the following code  

	import pubsubchannel
	import json
	def callback(data):
	  print json.dumps(data)
	channel = pubsubchannel()
	channel.subscribe("demo")
	channel.listen(callback=callback)

The callback will be called in a separate thread. To stop listening to events call

	channel.stop()

Subscribe may be called any number of times but listen should only be called once per client.
To send events call

	channel.publish("demo",message)

where message must be a json serializable object.
Note, the App Engine TaskQueue API is used internally but it is not exposed in the REST API
used by the python client, hence the app engine auth rules do not apply.
The python client depends on the requests package which can be installed with

	pip install requests

Curl REST Demo clients
-------
Two scripts are included to demonstrate the REST API using Curl.

	clients/subscribe channel

where channel is the channel you want to subscribe to.

	clients/publish channel json

where json is a json encoded string.

Examples
-------

[Hello World] (http://patompa.github.io/pubsubchannel/helloworld.html)

[Group Canvas] (http://patompa.github.io/pubsubchannel/groupcanvas.html?group=demo)

[![endorse](https://api.coderwall.com/patompa/endorsecount.png)](https://coderwall.com/patompa)



