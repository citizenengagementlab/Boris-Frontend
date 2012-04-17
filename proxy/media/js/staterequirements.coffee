
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
      ### Handle Required Fields ###
      ### Handle Help Text ###
      ### Handle ID Validation ###
      ### Handle SOS Contact Info ###
      ### Callback to advance form ###
    error: (error) ->
      ### Handle Error ###
  })