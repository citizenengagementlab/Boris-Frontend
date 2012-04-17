
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


getStateRequirements = () ->
  apiUrl = ""
  url = ""
  data = {}
  data["'home_zip_code'"] = $('#home_zip_code').val()
  data["'lang'"] = "en"
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
      

      ### Handle ID Validation ###
      minLength = response.id_min_length || 0
      maxLength = response.id_max_length || 100
      $('#id_number').attr('data-maxlength', maxLength).attr('data-minlength', minLength)

      ### Handle SOS Contact Info ###


      ### Callback to advance form ###
    error: (error) ->
      ### Handle Error ###
  })