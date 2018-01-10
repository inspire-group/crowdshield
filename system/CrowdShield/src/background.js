function BrowserActionButton() {

}

BrowserActionButton.prototype.getTwitterURLFromClick = function()
{
	var user = prompt("Enter user name (e.g. barackobama)");
	var end = prompt("Enter end time in specific format (yyyy-mm-dd)");
	var query = "https://twitter.com/search?l=&q=";
	query += "to:" + user + " until:" + end;
	var twitterURL = encodeURI(query);
	return twitterURL;
}


BrowserActionButton.prototype.launchExtension = function(twitterURL, callBack)
{
	// TODO: Can probably use message passing here with inject.js to pass db_name parameter
	chrome.tabs.create({url: twitterURL}, function(tab) {
		chrome.tabs.executeScript(tab.id, {file: "lib/js.js"});
		chrome.tabs.executeScript(tab.id, {file: "src/content.js"}, callBack);
	});
}


BrowserActionButton.prototype.setupServerConnection = function()
{
	chrome.runtime.onConnect.addListener(function(port) {
		var xhr = new XMLHttpRequest();
		port.onMessage.addListener(function(tweet) {
			console.log("Listened to tweet!");
			console.log(tweet);
			port.postMessage({question: "I don't get it."});
		});
	});
}

BrowserActionButton.prototype.getStartDate = function()
{

}

/******************************************************************************/

function Server() {

}

Server.prototype.onConnect = function()
{

}

Server.prototype.labelTweet = function() {

}


/******************************************************************************/

var main = function()
{
	chrome.browserAction.onClicked.addListener(function(tab) {
		var bab = new BrowserActionButton();
		var twitterURL = bab.getTwitterURLFromClick();
		bab.launchExtension(twitterURL, bab.setupServerConnection);
	});
};

main();
