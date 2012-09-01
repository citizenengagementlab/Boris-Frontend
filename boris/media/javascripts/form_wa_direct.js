function showStateRegContinueButtons() {
  if ($("input:radio[name='registrant[has_state_license]']:checked").val()=='1') {
      $('.has_no_license').hide();
      $('.has_license').show();
  } else if ($("input:radio[name='registrant[has_state_license]']:checked").val()=='0') {
      $('.has_license').hide();
      $('.has_no_license').show();
  }
}

function redirectToRegularForm() {
   //serialize values input so far
  var formValues = $('form input[name!=csrfmiddlewaretoken]').serialize();
  //redirect to regular form
  window.location.replace('/registrants/new/?state=WA&no_redirect&'+formValues);
}

$(document).ready(function() {
  $('.has_license').hide();

  showStateRegContinueButtons();
  $('#registrant_has_state_license_1, #registrant_has_state_license_0').click(showStateRegContinueButtons);

  $('form.registration-form').submit(function(event) {
    event.preventDefault(); //don't actually submit the form

    if ($("input:radio[name='registrant[has_state_license]']:checked").val()=='1') {
      //hide initial form
      $('form.registration-form').hide();

      //add disclaimer
      $('#content').append("<p class='explanation'>You can complete your voter registration online with Washington " +
          "using the form below. If your driver's license or state identification card is invalid " +
          "or the state can't find or confirm your DMV record, don't worry—you can also <a href='javascript:redirectToRegularForm()'>" +
          "finish your registration with Rock the Vote</a>. You will just have to print, sign, and mail it in.</p>");

      //add WA state iframe
      var fn = $('input#first_name').val();
      var ln = $('input#last_name').val();
      var dob = $('input#date_of_birth').val();
      $('#content').append('<iframe src="https://weiapplets.sos.wa.gov/myvote/myvote?'+
        'language=en&amp;Org=RocktheVote&amp;'+
        'firstname='+fn+'&amp;lastName='+ln+'&amp;DOB='+encodeURIComponent(dob)+
        '" width="600" height="725"></iframe>');

      //TODO:
      //submit partial registration to RTV for tracking
    } else if ($("input:radio[name='registrant[has_state_license]']:checked").val()=='0') {
       redirectToRegularForm();
    }

  });
});