var fbAppID = '347566241989371';
var fbAppUrl = 'https://apps.facebook.com/rockthevotenow/';
$('#content').css('opacity',0);
   
function preAuthView() {
  var pA = ['<div id="non-auth">'];
  pA.push('<a id="fb-auth" class="button button-primary" style="float: left; margin: 30px 0 0 143px;" href="');
  pA.push('https://www.facebook.com/dialog/oauth?client_id=');
  pA.push(fbAppID);
  pA.push('&redirect_uri=');
  if (window.location.search.length) {
    pA.push(encodeURIComponent(fbAppUrl+window.location.search+'&autosubmit=true'));
  } else {
    pA.push(encodeURIComponent(fbAppUrl+'?autosubmit=true'));
  }
  pA.push('&scope=email,user_birthday,user_location');
  pA.push('" target="_top">Register via Facebook</a>');
  pA.push('<p style="margin: 15px 0; float: left; clear: both; width: 100%; text-align: center;">- OR -</p>');
  pA.push('<a style="font-size: 16px; font-weight: bold; margin: 0; float: left; clear: both; width: 100%; text-align: center;" href="');
  if (getParam('facebook') == 1) {
    var ind = window.location.search.indexOf('facebook'); 
    var qStr = window.location.search.slice(0,ind)+window.location.search.slice(ind+11);
    if (qStr === "?") qStr = "";
    pA.push("https://"+window.location.host+qStr);
  } else {
    pA.push(window.location.href);
  }
  
  pA.push('" target="_top">Register on RockTheVote.com</a>');
  pA.push('<p style="margin: 30px 0; float: left; clear: both; width: 100%; text-align: center; font-size:16px;">');
  pA.push('Already registered? <a href="/registrants/share/">Share with your friends</a></p>');
  pA.push('</div>');
  $('#content').html(pA.join(""));
};

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

function checkInfo(user){
  if ($('form.state-form').length) {
    if (getParam("home_zip_code") !== "") {
      var zip = getParam("home_zip_code");
      $.ajax({
        type: 'get',
        url: '/usps/zip_lookup/',
        data: {
          zip: zip
        },
        success: function(d) {
          if (d.state) {
            $('select[name="state"]').val(d.state).focus();
            $('#map path').attr('fill','transparent').filter('path#jqvmap1_'+d.state.toLowerCase()).attr('fill','#21CB00');
            $('form.state-form').append('<input type="hidden" name="home_zip_code" value="'+zip+'" />');
            checkVals();
          }
        }
      });
    } else if (user && user.hasOwnProperty("location")) {
      if (user.locale == "en_US") {
        function stateAbbr(stateName) {
          switch (stateName.toUpperCase()) {
              case "ALABAMA": return "AL";
              case "ALASKA": return "AK";
              case "ARIZONA": return "AZ";
              case "ARKANSAS": return "AR";
              case "CALIFORNIA": return "CA";
              case "COLORADO": return "CO";
              case "CONNECTICUT": return "CT";
              case "DELAWARE": return "DE";
              case "DISTRICT OF COLUMBIA": case "DISTRICT": return "DC";
              case "FLORIDA": return "FL";
              case "GEORGIA": return "GA";
              case "HAWAII": return "HI";
              case "IDAHO": return "ID";
              case "ILLINOIS": return "IL";
              case "INDIANA": return "IN";
              case "IOWA": return "IA";
              case "KANSAS": return "KS";
              case "KENTUCKY": return "KY";
              case "LOUISIANA": return "LA";
              case "MAINE": return "ME";
              case "MARYLAND": return "MD";
              case "MASSACHUSETTS": return "MA";
              case "MICHIGAN": return "MI";
              case "MINNESOTA": return "MN";
              case "MISSISSIPPI": return "MS";
              case "MISSOURI": return "MO";
              case "MONTANA": return "MT";
              case "NEBRASKA": return "NE";
              case "NEVADA": return "NV";
              case "NEW HAMPSHIRE": return "NH";
              case "NEW JERSEY": return "NJ";
              case "NEW MEXICO": return "NM";
              case "NEW YORK": return "NY";
              case "NORTH CAROLINA": return "NC";
              case "NORTH DAKOTA": return "ND";
              case "OHIO": return "OH";
              case "OKLAHOMA": return "OK";
              case "OREGON": return "OR";
              case "PALAU": return "PW";
              case "PENNSYLVANIA": return "PA";
              case "RHODE ISLAND": return "RI";
              case "SOUTH CAROLINA": return "SC";
              case "SOUTH DAKOTA": return "SD";
              case "TENNESSEE": return "TN";
              case "TEXAS": return "TX";
              case "UTAH": return "UT";
              case "VERMONT": return "VT";
              case "VIRGINIA": return "VA";
              case "WASHINGTON": return "WA";
              case "WEST VIRGINIA": return "WV";
              case "WISCONSIN": return "WI";
              case "WYOMING": return "WY";
              default: return "";
          }
        }
        
        var loc = user.location.name.split(", ");
        var abbr = stateAbbr(loc[1]);
        if (abbr !== "") {
          $('select[name="state"]').val(abbr).focus();
          $('#map path').attr('fill','transparent').filter('path#jqvmap1_'+abbr.toLowerCase()).attr('fill','#21CB00');
        }
          
      }
    }

    if (getParam("email_address") !== "") {
      $('input[name="email_address"]').val(getParam("email_address"));
    } else if (user && user.hasOwnProperty('email')) {
      $('input[name="email_address"]').val(user.email);
    }
    
    
    
    function checkVals(){
      if ($('input[name="email_address"]').val() !== "" && $('input[name="email_address"]').val() !== $('input[name="email_address"]').attr('placeholder')) {
        if ($('select[name="state"]').val() !== "Select State...") {
          $('form.state-form button').prop('disabled', false);
          if (getParam("autosubmit") == 'true' && getParam("autosubmitoverride") != 'true') {
            //$('form.state-form').submit();
          }
        }
      }
    }
    checkVals();
  } else if ($('form.registration-form').length) {
    if (user) {
      if (user.hasOwnProperty('first_name') && getParam('first_name') === "")
        $('input[name="first_name"]').val(user.first_name);
      
      if (user.hasOwnProperty('last_name') && getParam('last_name') === "")
        $('input[name="last_name"]').val(user.last_name);
        
      if (user.hasOwnProperty('birthday') && getParam('date_of_birth') === "")
        $('input[name="date_of_birth"]').val(user.birthday);
        
      if (user.hasOwnProperty('email') && getParam("email_address") === "")
        $('input[name="email_address"]').val(user.email);
      if (user.hasOwnProperty('gender')) {
        var ut = (user.gender === 'female') ? "Ms." : "Mr.";
        $('select[name="name_title"]').val(ut).focus().blur();
      }
    }
    
    
  }

};
  
  
  
// Init the SDK upon load
window.fbAsyncInit = function() {
  FB.init({
    appId      : fbAppID, // App ID
    status     : true, // check login status
    cookie     : true, // enable cookies to allow the server to access the session
    xfbml      : true  // parse XFBML
  });
  
  FB.Canvas.setAutoGrow();
  
  function statusCheck(response){
    if (response.authResponse) {
      FB.api('/me', function(me){
        if (me.name)
          checkInfo(me);
      });
      
    } else {
      preAuthView();
    }
    $('#content').css('opacity',1);
  }
  
  if (getParam("request_ids") !== "") {
    //delete accepted requests, if desired
    //FB.api(getParam("request_ids"), 'delete', function(response){ console.log(response) });
  }

  if (getParam("facebook") == 1) {
    
    if ($('form').length) {
      $('form').append('<input type="hidden" name="facebook" value="1" />');
    }

    FB.getLoginStatus(function(response) { statusCheck(response); });
         
    //possible TODO - handle cases where user removes authorization with app still open
    FB.Event.subscribe('auth.statusChange', function(response) { statusCheck(response); });

  } else {
    //not on facebook iframe
    if (window.location.search.length) checkInfo();
    $('#content').css('opacity',1);
  }
};

(function() {
   var e = document.createElement('script'); e.async = true;
   e.src = document.location.protocol +
     '//connect.facebook.net/en_US/all.js';
   document.getElementById('fb-root').appendChild(e);
}());