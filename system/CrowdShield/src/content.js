function TweetMentionsPage(port)
{
	this._port = port;
	this._tweets = [];

	//this.scrollListen();

	this.addAbusiveButtons = function(callBack)
	{
		// Construction of abuse button
		var $li_abusive = $('<li>', {"class": "button-abusive", "role": "presentation"});
		var $button_abusive = $('<button>', {"class": "dropdown-link", "type": "button", "role": "menuitem", "text": "Mark Tweet Abusive"});
		$li_abusive.append($button_abusive);

		// Adding buttons to tweet dropdown menu
		var $ul = $('.ProfileTweet-action > .dropdown > .dropdown-menu > ul');
		$ul.prepend($li_abusive);

		// Assign callBack function to clicking on buttons
		var $abusive = $('.button-abusive');
	  $abusive.click({abusive: 1}, callBack);
	}

	this.addBenignButtons = function(callBack)
	{
		// Construction of benign button
		var $li_benign = $('<li>', {"class": "button-benign", "role": "presentation"});
		var $button_benign = $('<button>', {"class": "dropdown-link", "type": "button", "role": "menuitem", "text": "Mark Tweet Benign"});
		$li_benign.append($button_benign);

		// Adding buttons to tweet dropdown menu
		var $ul = $('.ProfileTweet-action > .dropdown > .dropdown-menu > ul');
		$ul.prepend($li_benign);

		// Assign callBack function to clicking on buttons
		var $benign = $('.button-benign')
		$benign.click({abusive: 0}, callBack);
	}

	this.callServer = function(event)
	{
		console.log(event.data);
		var port = this._port;
		var abusive = event.data.abusive;
		var tweetData = event.target.closest('.tweet');
		var tweet = new Tweet(tweetData);
		port.postMessage({tweet: tweet});
	}
}


TweetMentionsPage.prototype.getTweets = function()
{

}


TweetMentionsPage.prototype.scrollListen = function()
{
	$( window ).scroll(function() {
	  $( "span" ).css( "display", "inline" ).fadeOut( "slow" );
	});
}


TweetMentionsPage.prototype.markTweets = function()
{

}




/******************************************************************************/

function Tweet(tweet)
{
  this.id = tweet.attributes['data-tweet-id'].value;
  this.date = tweet.getElementsByClassName('tweet-timestamp')[0].getAttribute('title');
  this.username = tweet.getElementsByClassName('username')[0].getElementsByTagName('b')[0].textContent;

  // Text related information
  this.text = tweet.getElementsByClassName('tweet-text')[0].textContent;
  this.lang = tweet.getElementsByClassName('tweet-text')[0].getAttribute('lang');
  var links_list = tweet.getElementsByClassName('twitter-timeline-link');
  this.links = $(links_list).map(function(){return $(this).text();}).get();
}

Tweet.prototype.addButton = function()
{

}

Tweet.prototype.markAbusiveness = function()
{

}

Tweet.prototype.onButtonClick = function(tweet, url)
{
	$('a').click( function() {
		//get the url
		var url = $(this).prop('href');
		//send the url to your server
		$.ajax({
		  type: "POST",
		  url: "localhost:55555",
		  data: tweet
		});
	});
}

/******************************************************************************/

var main = function()
{
	var port = chrome.runtime.connect();
	tmp = new TweetMentionsPage(port);
	tmp.addAbusiveButtons(tmp.callServer);
	//tmp.addButtons(tmp.callServer);
}

main();
