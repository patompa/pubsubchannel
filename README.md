pubsubchannel
=============

A Hosted Publish Subscribe Event Channel on Google App Engine using Channels

Javascript Frontend
-------

Add:
```html
	<script type="text/javascript" src="http://pubsubchannel.appspot.com/"></script>
```

where pubsubchanel is the app id of your Google App Engine application where the 
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




