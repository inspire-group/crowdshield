// TODO: Clean up namespace, remove or keep error + success logs?
var db_holder = function() {
  var db_holder = {};
  var dbName = $('.ProfileCard')[0].attributes['data-screen-name'].value;
  var DBOpenRequest = window.indexedDB.open(dbName, 1);
  DBOpenRequest.onsuccess = function(event) {
    db_holder.db = DBOpenRequest.result;
  }
  DBOpenRequest.onupgradeneeded = function(event) {
    var db = event.target.result;
    db.createObjectStore("tweets", { keyPath: "id" }); //TODO: Possibly add object store reference here
  };
  return db_holder;
}();


// HACK: To get tweet_data values + db, maybe modularize process later?
function store_tweet(event) {
  /*
    Call-back function for taking a tweet and storing it once clicked on
  */
  // Abusiveness
  var abusive = event.data.abusive

  // Metadata related information
  var tweet = event.target.closest('.tweet');
  var id = tweet.attributes['data-tweet-id'].value;
  var date = tweet.getElementsByClassName('tweet-timestamp')[0].getAttribute('title');
  var username = tweet.getElementsByClassName('username')[0].getElementsByTagName('b')[0].textContent;

  // Text related information
  var text = tweet.getElementsByClassName('tweet-text')[0].textContent;
  var lang = tweet.getElementsByClassName('tweet-text')[0].getAttribute('lang');
  var links_list = tweet.getElementsByClassName('twitter-timeline-link');
  var links = $(links_list).map(function(){return $(this).text();}).get();

  // Construction and storage of json
  var tweet_data = {id: id, text: text, date: date, username: username, links: links, lang: lang, abusive: abusive};
  var objectStore = db_holder.db.transaction("tweets", "readwrite").objectStore("tweets");
  objectStore.put(tweet_data);

  tweet.setAttribute('tweet-is-negative', !!abusive);
  // TODO: Add bert_processed to class for tweet_text??
}


// TODO: Make sure button is added to new tweets that are loaded onto screen as well
function tweet_buttons() {
  /*
    Adds button options to tweets on user's page
  */
  // Construction of abuse button
  var $li_abusive = $('<li>', {"class": "button-abusive", "role": "presentation"});
  var $button_abusive = $('<button>', {"class": "dropdown-link", "type": "button", "role": "menuitem", "text": "Mark Tweet Abusive"});
  $li_abusive.append($button_abusive);

  // Construction of benign button
  var $li_benign = $('<li>', {"class": "button-benign", "role": "presentation"});
  var $button_benign = $('<button>', {"class": "dropdown-link", "type": "button", "role": "menuitem", "text": "Mark Tweet Benign"});
  $li_benign.append($button_benign);

  // Adding buttons to tweet dropdown menu
  var $ul = $('.ProfileTweet-action > .dropdown > .dropdown-menu > ul');
  $ul.prepend($li_abusive);
  $ul.prepend($li_benign);

  var $abusive = $('.button-abusive');
  // TODO: Testing
  //$abusive.click({abusive: 1}, callBackground);
  $abusive.click({abusive: 1}, store_tweet);

  var $benign = $('.button-benign')
  // TODO: Testing
  //$benign.click({abusive: 0}, callBackground);
  $benign.click({abusive: 0}, store_tweet);
}


// TODO: Should look at stuff
function process_tweets() {
  var objectStore = db_holder.db.transaction("tweets", "readonly").objectStore("tweets");
  $('.tweet-text').not('.bert_processed').each(function(i, node) {
      var tweet = node.closest('.tweet');
      var id = tweet.attributes['data-tweet-id'].value;
      var req = objectStore.openCursor(id);
      req.onsuccess = function(e) {
        var cursor = e.target.result;
        if (cursor) {
          tweet.setAttribute('tweet-is-negative', !!cursor.value.abusive);
        } else {
          // TODO: Replace with nlp algorithm or something
          tweet.setAttribute('tweet-is-negative', false);
        }
      };
      req.onerror = function(e) {
        alert("ERROR");
      };
      node.className += ' bert_processed';
  })
}


function callBackground(event) {
  /*
    Call-back function called when tweet is clicked on for abusive or benign
  */
  // Metadata related information
  var tweet = event.target.closest('.tweet');
  // TODO: Testing whether or not callback will work
  /*
  chrome.extension.sendMessage({from: 'content', tweet: 'tweet'}, function(response) {
        console.log(response);
  });*/
  chrome.extension.sendMessage({greeting: "hello"}, function(response) {
    console.log(response.farewell);
  });
}
