/*
  author: Albert Ho

  Background script to launch the extension
  -> Add a listener to connect to the server / port after executing script
  -> Setup a port connection to a server in Python
*/


chrome.browserAction.onClicked.addListener(function(tab) {
  /*
    Called on clicking Browser Action button to launch extension
  */
  var user = prompt("Enter user name (e.g. barackobama)");
  //var start = prompt("Enter start time in specific format (yyyy-mm-dd)");
  var end = prompt("Enter end time in specific format (yyyy-mm-dd)");

  var query = "https://twitter.com/search?l=&q=";
  query += "to:" + user + " until:" + end;
  //query += "to:" + user + " since:" + start + " until:" + end;
  twitterURL = encodeURI(query);

  // TODO: Can probably use message passing here with inject.js to pass db_name parameter
  chrome.tabs.create({url: twitterURL}, function(tab) {
    console.log("loaded!");
    /*
    chrome.tabs.executeScript(tab.id, {file: "src/button.js", runAt: "document_end"});
    chrome.tabs.executeScript(tab.id, {file: "src/afinn.js", runAt: "document_end"});
    chrome.tabs.executeScript(tab.id, {file: "src/abp.js", runAt: "document_end"});
    chrome.tabs.executeScript(tab.id, {file: "src/run.js", runAt: "document_end"});
    */
    chrome.tabs.executeScript(tab.id, {file: "src/inject.js"});
    // TODO: Add a listener to a port connection
    // var port = chrome.tabs.connect(tab.id, {name: "knockknock"});
    //alert("CREATED PORT" + port);
    alert("HELLO HELLO: INSIDE BACKGROUND.JS");
    chrome.runtime.onConnect.addListener(function(port) {
      console.log("INSIDE ONCONNECT IN BACKGROUND.JS");
      alert("HELLO!");
      console.assert(port.name == "knockknock");
      port.onMessage.addListener(function(msg) {
        if (msg.joke == "Knock knock")
          port.postMessage({question: "Who's there?"});
        else if (msg.answer == "Madame")
          port.postMessage({question: "Madame who?"});
        else if (msg.answer == "Madame... Bovary")
          port.postMessage({question: "I don't get it."});
      });
    });
  });
});

alert("Exiting background.js?");

/*
var connectToTwitter = chrome.tabs.onConnect.addListener(function (port) {
  var tab = port.sender.tab;
  console.log("LINE 35 in BACKGROUND.JS");
  // This will get called by the content script we execute in
  // the tab as a result of the user pressing the browser action.
  port.onMessage.addListener(function(info) {
    console.log(info);
    alert(info);
  });
});*/
