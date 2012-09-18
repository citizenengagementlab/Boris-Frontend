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
  var state = $('form.registration-form input#home_state_id').val();
  window.location.replace('/registrants/new/?state='+state+'&no_redirect&'+formValues);
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

      //show disclaimer
      $('#state-explanation').show();

      //add state iframe
      add_state_iframe(); //function defined in template, so we can reuse this file for multiple states

      //TODO:
      //submit partial registration to RTV for tracking
    } else if ($("input:radio[name='registrant[has_state_license]']:checked").val()=='0') {
       redirectToRegularForm();
    }

  });
});