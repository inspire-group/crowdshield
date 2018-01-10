chrome.extension.sendMessage({}, function(response) {
	/*
	  Injects the contents of other scripts into the web page
	*/
	var readyStateCheckInterval = setInterval(function() {
	if (document.readyState === "complete") {
		clearInterval(readyStateCheckInterval);

		console.log("INSERTING SCRIPTS");

	  ['button.js', 'afinn.js', 'abp.js', 'run.js'].map(function(script) {
	      var s = document.createElement('script');
	      s.src = chrome.extension.getURL('src/' + script);
	      s.onload = function() {
	          this.parentNode.removeChild(this);
	      };
	      (document.head||document.documentElement).appendChild(s);
	  });
	}
	}, 10);

	/*
	const id = "ffphgcjmchcdbhjgclbdimolmokabjho";
	var port = chrome.runtime.connect(id, {name: "knockknock"});
	port.postMessage({joke: "Knock knock"});
	port.onMessage.addListener(function(msg) {
	  if (msg.question == "Who's there?")
	    port.postMessage({answer: "Madame"});
	  else if (msg.question == "Madame who?")
	    port.postMessage({answer: "Madame... Bovary"});
	});*/
});
