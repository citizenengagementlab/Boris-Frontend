function addFloodlightTrackingPixel() {
/*
  Start of DoubleClick Floodlight Tag: Please do not remove
  Activity name of this tag: Rock The Vote Conversion Pixel
  URL of the webpage where the tag is expected to be placed: http://www.rockthevote.com/

  This tag must be placed between the <body> and </body> tags, as close as possible to the opening tag.
  Creation Date: 10/05/2012
  */
  var axel = Math.random() + "";
  var a = axel * 10000000000000;
  $('body').append('<iframe src="https://fls.doubleclick.net/activityi;src=3838314;type=rtvco381;cat=rockt950;ord=' + a + '?" width="1" height="1" frameborder="0" style="display:none"></iframe>');
}

function showStateRegContinueButtons() {
  if ($("input#registrant_has_state_license_1:checked").val()=='1') {
      $('.has_no_license').hide();
      $('.has_license').show();
  } else {
      $('.has_license').hide();
      $('.has_no_license').show();
  }
}

function redirectToRegularForm() {
   //serialize values input so far
  var formValues = $('form input[name!=csrfmiddlewaretoken], form select').serialize();
  //redirect to regular form
  var state = $('form.registration-form input#home_state_id').val();
  window.location.replace('/registrants/new/?state='+state+'&no_redirect=1&'+formValues);
}

function submitPartialToRocky() {
  //submit partial registration to RTV for tracking
  var formValues = $('form input[name!=csrfmiddlewaretoken], form select').serialize();
  var submitURL = $('form').attr('action');
  $.ajax({
    type:'POST',
    url:submitURL,
    data: formValues,
    success: continueToStateForm
  });
}

function continueToStateForm() {
  //hide initial form
  $('form.registration-form').hide();

  //show state explanation
  $('.explanation#state').show();

  //function defined in template, so we can reuse this file for multiple states
  add_state_iframe();
  
  //add tracking pixel for floodlight
  //addFloodlightTrackingPixel();
  
  //show share buttons
  $('body').addClass('finish');
  $('.share').show();
  $('#share-link').hide();
}

$(document).ready(function() {
  $('.has_license').hide();

  showStateRegContinueButtons();
  $('#registrant_has_state_license_1, #registrant_has_state_license_0').click(showStateRegContinueButtons);

  $('form.registration-form').submit(function(event) {
    event.preventDefault(); //don't actually submit the form

    if ($("input#registrant_has_state_license_1:checked").val()=='1') {
      submitPartialToRocky();
    } else {
       redirectToRegularForm();
    }

  });
});