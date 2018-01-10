//document.styleSheets[0].insertRule("[tweet-is-negative=true]{display:none}", 0);

tweet_buttons();
document.styleSheets[0].insertRule("[tweet-is-negative=true]{background-color:rgba(255, 0, 0, 0.4)}", 0);
document.styleSheets[0].insertRule("[tweet-is-negative=false]{background-color:rgba(0, 255, 0, 0.4)}", 0);

//chrome.tabs.connect();
//setInterval(tweet_buttons, 2000); //HACK: Creates tweet buttons for new tweets by refreshing timer

/*
var additionalInfo = {
  "testing": "Hello? I am in here!!!"
};

var port = chrome.runtime.connect(id);
console.log("here is a port: " + port);
port.postMessage(additionalInfo);
*/

const id = "ffphgcjmchcdbhjgclbdimolmokabjho";
var port = chrome.runtime.connect(id, {name: "knockknock"});
port.postMessage({joke: "Knock knock"});
port.onMessage.addListener(function(msg) {
  if (msg.question == "Who's there?")
    port.postMessage({answer: "Madame"});
  else if (msg.question == "Madame who?")
    port.postMessage({answer: "Madame... Bovary"});
});

setInterval(process_tweets, 2000);
//test_tweets();
//setInterval(store_tweets, 200);
