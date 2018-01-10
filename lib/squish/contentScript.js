var threshold = 50;//if sync.get fails, we use 50 as a default.

chrome.storage.sync.get({
  threshold: '50'
}, function(items) {
  threshold = items.threshold;
});

//deal with newly loaded tweets
function DOMModificationHandler(){
    $(this).unbind('DOMSubtreeModified.event1');
    setTimeout(function(){
        modify();
        $('#timeline').bind('DOMSubtreeModified.event1',DOMModificationHandler);
    },10);
}
$('#timeline').bind('DOMSubtreeModified.event1',DOMModificationHandler);


// Classify tweets based on abusive content
function classify(t){
  chrome.runtime.sendMessage({message: "listeners"}, function(response) {
  });
}


function modify(){
  //find and modify tall tweets
  $('.tweet-text').each(function(index){
    var t = $(this).text();
    var isOffensive = classify(t)
    if(!$(this).hasClass("offensive") && isOffensive){
      $(this).addClass("offensive");
      $(this).html(`<button class="crowdshield-button EdgeButton EdgeButton--primary" data-original-content="${encodeURI(t)}">Show Shielded Tweet</button>`);
      //if we add a new button, we have to add listeners again...
      chrome.runtime.sendMessage({message: "listeners"}, function(response) {
      });
    }
  });
}

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
