window['PubSub'] = function () {

  var token;
  var APP_ID = "http://pubsubchannel.appspot.com";
  var RENEW_INTERVAL = 60000;
  var namespace = "";
  
  function S4() {
           return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
     }

  function guid() {
           return (S4() + S4() + S4() + S4() + S4() + S4() + S4() + S4());
  }

  var clientId = "PULL_" + guid();

  function id() {
	  return clientId;
  }
  function setNamespace(ns) {
	  namespace = ns;
  }

  function setAppID(app) {
          APP_ID = app;
  }

  function getNS() {
      var nsparam = "";
      if (namespace !=+ "") {
	      nsparam = "&namespace=" + namespace;
      }
      return nsparam;
  }

  function subscribe(group, callback) {
      $.getJSON(APP_ID + '/subscribe?group=' + group + "&client=" + clientId + getNS(), function(result) {
			   token = result.token;
			   poll(callback);
                           setTimeout(function() {renew(group)},RENEW_INTERVAL);
               });
  }

  function renew(group) {
      $.getJSON(APP_ID + '/subscribe?group=' + group + "&client=" + clientId + getNS(), function(result) {
		      console.log(result);
      });
      setTimeout(function() {renew(group)},RENEW_INTERVAL);
  }

  function poll(callback) {
      $.getJSON(APP_ID + '/pull?client=' + clientId + getNS(), function(result) {
	   try {
	      for (var i=0; i < result.messages.length; i++) {
	           callback(result.messages[i]);
              }
	      if (result.messages.length == 0) {
		      console.log("TIMEOUT " + new Date());
	      }
	   } catch(exception) {
	      console.log("Poll Error " + exception);
	   }
           setTimeout(function () {poll(callback)},1);
      }).error(function(jqXHR, textStatus, errorThrown) {
           console.log("error " + textStatus);
           console.log("incoming Text " + jqXHR.responseText);	  
	   setTimeout(function() {poll(callback)},5000) 
	});

  }

  function publish(group,json) {
   $.ajax({url:APP_ID + '/publish?group=' + group + "&token=" + token + getNS(),
	   data: JSON.stringify(json),
           type: "POST",
           beforeSend: function(xhr) {
	      xhr.setRequestHeader('Content-Type','application/json');
	   }});
  }

  return {'id':id,
	  'setNamespace': setNamespace,
	  'setAppID': setAppID,
	  'subscribe': subscribe,
	  'publish': publish };

}();

