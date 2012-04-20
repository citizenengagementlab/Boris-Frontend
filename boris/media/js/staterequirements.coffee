showRegistrationForm = () ->
  firstName = $('#pre_first_name').val()
  lastName  = $('#pre_last_name').val()
  email     = $('#pre_email_address').val()
  zip       = $('#pre_zip_code').val()
  $('#first_name').val(firstName)
  $('#last_name').val(lastName)
  $('#email_address').val(email)
  $('#home_zip_code').val(zip)
  $('#state_form').hide()
  $('#registration_form').show()

getCityState = (zip) ->
  $.ajax
    type: 'get'
    url: '/usps/zip_lookup/'
    data:
      zip: zip
    success: (d) ->
      ### Handle City and State Data ###
      #zipCode = $("#pre_zip_code").val()
      #alert(zipCode)
      homeCity = d.city
      homeState = d.state

      #$("#home_zip_code").val(zipCode)
      $("#home_city").val(homeCity)
      $("#home_state_id").val(homeState)
      getStateRequirements()
    error: (error) ->
      ### TODO: Handle Error ###

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
        if response.no_party_msg.toLowerCase() == "decline to state"
          html += "<option val=\"Decline to state\">Decline to state</option>\n"
        ### append HTML ###
        $target.append(html)
      
      ### Handle Required Fields ###
      if response.requires_party
        $('#party').attr('data-required', true);
      if response.requires_party
        $('#party').attr('data-required', true);
      
      ### Handle Help Text ###
      if response.id_number_msg
        $('#tooltip_text_id_number').text(response.id_number_msg)
      if response.requires_party_msg
        $('#tooltip_text_party').text(response.requires_party_msg)
      if response.requires_race_msg
        $('#tooltip_text_race').text(response.requires_race_msg)

      ### Handle ID Validation Requirements ###
      minLength = response.id_min_length || 0
      maxLength = response.id_max_length || 100
      $('#id_number').attr('data-maxlength', maxLength).attr('data-minlength', minLength)

      ### Handle SOS Contact Info (where is this used?) ###


      ### Callback to advance form ###
      showRegistrationForm()

    error: (error) ->
      ### TODO: Handle Error ###
  })