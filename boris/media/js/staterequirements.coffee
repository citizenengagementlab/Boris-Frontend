
getCityState = (zip) ->
  $.ajax
    type: 'get'
    url: '/usps/zip_lookup/'
    data:
      zip: zip
    success: (data) ->
      ### Handle City and State Data ###
      $("form#ovr #home_zip_code").val data.zip
      $("form#ovr #home_city").val data.city
      $("form#ovr #home_state_id").val data.state
    error: (error) ->
      ### Handle Error ###

showRegistrationForm = () ->
  firstName = $('#pre_first_name').val()
  lastName  = $('#pre_last_name').val()
  email     = $('#pre_email_address').val()
  zip       = $('#pre_zip_code')  
  $('#first_name').val(firstName)
  $('#last_name').val(lastName)
  $('#email_address').val(email)
  $('#home_zip_code').val(zip)
  $('#state_form').hide()
  $('#registration_form').show()

getStateRequirements = () ->
  apiUrl = ""
  url = ""
  data = {}
  data["'home_zip_code'"] = $('#pre_zip_code').val()
  data["'lang'"] = $('#lang_id').val()
  $.ajax({
    url: apiUrl + url
    data: data
    type: 'get'
    success: (response) ->
      ### Handle Political Parties ###
      if response.party_list
        parties = response.party_list
        $target = $('select#party')
        html = ""
        for i in parties
          ### generate html ###
          party = parties[i]
          html += "<option val=#{party}>#{party}</option>\n"
        if response.no_party_msg == "Decline to state"
          html += "<option val=\"Decline to state\">Decline to state</option>\n"
        ### append HTML ###
        $target.append(html)
      
      ### Handle Required Fields ###
      if response.requires_party
        $('#party').attr('data-required', true);
      if response.requires_party
        $('#party').attr('data-required', true);
      
      ### TODO Handle Help Text ###
      

      ### Handle ID Validation Requirements ###
      minLength = response.id_min_length || 0
      maxLength = response.id_max_length || 100
      $('#id_number').attr('data-maxlength', maxLength).attr('data-minlength', minLength)

      ### Handle SOS Contact Info ###


      ### Callback to advance form ###
      showRegistrationForm()

    error: (error) ->
      ### Handle Error ###
  })