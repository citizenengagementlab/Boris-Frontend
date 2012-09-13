var fbAppID = '347566241989371';
var fbAppUrl = 'https://apps.facebook.com/rockthevotenow/';

function getParam(name){
  name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
  var regexS = "[\\?&]" + name + "=([^&#]*)";
  var regex = new RegExp(regexS);
  var results = regex.exec(window.location.search);
  if(results === null)
    return "";
  else
    return decodeURIComponent(results[1].replace(/\+/g, " "));
};

window.fbAsyncInit = function() {
  FB.init({
    appId      : fbAppID, // App ID
    status     : true, // check login status
    cookie     : true, // enable cookies to allow the server to access the session
    xfbml      : true  // parse XFBML
  });
};

$('a.button.facebook#facebook-app-share').click(function(){
  $b = $(this);
  var fGet = (getParam('partner_id') != "") ? "?partner_id="+getParam('partner_id') : "";
  var pObj = {
    'name' : "Rock the Vote 2012",
    'description' : "November will be here before you know it! Are you registered to vote? If not, now's the time! Register here - in 3 easy steps! - using Rock the Vote's online voter registration tool.",
    'media': [{
      "type": "flash", 
      //"swfsrc": "https://s3.amazonaws.com/rocky-boris-test/widgetloader/rtv_fb.swf?v="+(+new Date()), 
      "swfsrc": "https://"+window.location.hostname+"/static/widgetloader/rtv_fb.swf"+fGet, 
      //"imgsrc": "https://s3.amazonaws.com/rocky-boris-test/images/flash-preview.gif?v="+(+new Date()), 
      "imgsrc": "https://"+window.location.hostname+"/static/images/flash-preview.gif", 
      "width": "130",
      "height": "87",
      "expanded_width": "398",
      "expanded_height": "375"
    }]
    //'actions': [{ link: window.location.href, name: "RockTheVote.com" }]
  };

  FB.ui(
    {
      method: 'stream.publish',
      //message: 'Lorem ipsum',
      //user_message: 'test user message',
      attachment: pObj,
      user_message_prompt: 'Tell your friends to register!'
    },
    function(response) {
      if (response.hasOwnProperty("post_id")) {
        $b.html("Send Requests!").unbind('click').click(function(){
          FB.ui({method: 'apprequests',
            message: 'Become a registered voter!'
          }, function(response){
            if (response.hasOwnProperty("request")){
              $b.html("Thanks for sharing!").attr('disabled',true).css('opacity',0.4).unbind('click');
            } else {
              alert("There was an error in sending your requests. Please try again.");
            }
          });
        });
      } else {
        alert("There was an error in publishing your post. Please try again.");
      }
    }
  );
 
});

// Load the SDK Asynchronously
(function(d){
   var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
   if (d.getElementById(id)) {return;}
   js = d.createElement('script'); js.id = id; js.async = true;
   js.src = "//connect.facebook.net/en_US/all.js";
   ref.parentNode.insertBefore(js, ref);
 }(document));