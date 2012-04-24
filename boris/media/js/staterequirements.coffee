showRegistrationForm = () ->
  firstName = $('#pre_first_name').val()
  lastName  = $('#pre_last_name').val()
  email     = $('#pre_email_address').val()
  zip       = $('#pre_zip_code').val()
  $('#first_name').val(firstName)
  $('#last_name').val(lastName)
  $('#email_address').val(email)
  $('#home_zip_code').val(zip)
  
  switch window.LAYOUT
    when "singlepage"
      $('#state_form').hide()
      $('#registration_form').show()
    when "tabs"
      $("#get_started").hide()
      $("#address").show()
    when "accordion"
      $("#get_started > ul").slideUp()
      $("#address > ul").slideDown()



getCityState = (zip) ->
  $.ajax
    type: 'get'
    url: '/usps/zip_lookup/'
    data:
      zip: zip
    success: (d) ->
      ### Handle City and State Data ###
      if (d.state != undefined)
        homeCity = d.city
        homeState = d.state
        #$("#home_zip_code").val(zipCode)
        $("#home_city").val(homeCity)
        $("#home_state_id").val(homeState).attr('readonly','readonly')
      getStateRequirements()
      return true
    error: (xhr,status,error) ->
      ### Handle Error ###
      #console.log error
      $('#pre_zip_code')
        .addClass('error')
        .parent()
        .append("<p class='error-message'>Invalid zip code</p>")
        .children('.error-message')
        .hide()
        .fadeIn()
      $('form#get_started img.spinner').remove()
      return false

getStateRequirements = () ->
  url = "/rtv/api/v1/state_requirements.json"
  data = {
    'home_zip_code': $('#pre_zip_code').val()
    'lang': $('#lang_id').val()
  }
  $.ajax({
    url: url
    data: data
    type: 'get'
    success: (response) ->
      ### Handle Political Parties ###
      if response.party_list
        parties = response.party_list
        $target = $('select#party')
        html = ""
        for party in parties
          ### generate html ###
          html += "<option val=#{party}>#{party}</option>\n"
        if response.no_party_msg == "Decline to state"
          html += "<option val=\"Decline to state\">Decline to state</option>\n"
        ### append HTML ###
        $target.append(html)
      
      ### Handle Required Fields ###
      if response.requires_party
        $('#party').attr('data-required', true)
      if response.requires_party
        $('#party').attr('data-required', true)
      
      ### Handle Help Text ###
      if response.id_number_msg
        $('#tooltip_text_id_number').text(response.id_number_msg)
      if response.requires_party_msg
        $('#tooltip_text_party').text(response.requires_party_msg)
      if response.requires_race_msg
        $('#tooltip_text_race').text(response.requires_race_msg)

      ### Handle ID Validation Requirements ###
      minLength = response.id_length_min || 0
      maxLength = response.id_length_max || 100
      $('#id_number').attr('data-maxlength', maxLength).attr('data-minlength', minLength)

      ### TODO: Handle SOS Contact Info (where is this used?) ###

      ### Callback to advance form ###
      showRegistrationForm()

    error: (xhr,status,error) ->
      $('form#get_started img.spinner').hide()
      response = $.parseJSON(xhr.responseText)
      $('#state_form').before('<div class="error-message big-error"><h1>Sorry, you are not eligible to register to vote for the following reason(s):</h1><p>'+response.error.message+'</p></div>')
      $('#state_form').hide()
      $('#registration').hide()

  })