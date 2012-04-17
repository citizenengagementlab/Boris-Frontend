(function() {
  var getCityState, getStateRequirements, showRegistrationForm;

  getCityState = function(zip) {
    return $.ajax({
      type: 'get',
      url: '/usps/zip_lookup/',
      data: {
        zip: zip
      },
      success: function(data) {
        /* Handle City and State Data
        */        $("form#ovr #home_zip_code").val(data.zip);
        $("form#ovr #home_city").val(data.city);
        return $("form#ovr #home_state_id").val(data.state);
      },
      error: function(error) {
        /* Handle Error
        */
      }
    });
  };

  showRegistrationForm = function() {
    /* Show Registration Form
    */
    var email, firstName, lastName;
    firstName = $('#get_started #first_name').val();
    lastName = $('#get_started #last_name').val();
    email = $('#get_started #email').val();
    /* don't return true, return a real thing
    */
    return true;
  };

  getStateRequirements = function() {
    var apiUrl, data, url;
    apiUrl = "";
    url = "";
    data = {};
    data["'home_zip_code'"] = $('#home_zip_code').val();
    data["'lang'"] = "en";
    return $.ajax({
      url: apiUrl + url,
      data: data,
      type: 'get',
      success: function(response) {
        /* Handle Political Parties
        */
        var $target, html, i, maxLength, minLength, parties, party, _i, _len;
        if (response.party_list) {
          parties = response.party_list;
          $target = $('select#party');
          html = "";
          for (_i = 0, _len = parties.length; _i < _len; _i++) {
            i = parties[_i];
            /* generate html
            */
            party = parties[i];
            html += "<option val=" + party + ">" + party + "</option>\n";
          }
          if (response.no_party_msg === "Decline to state") {
            html += "<option val=\"Decline to state\">Decline to state</option>\n";
          }
          /* append HTML
          */
          $target.append(html);
        }
        /* Handle Required Fields
        */
        if (response.requires_party) $('#party').attr('data-required', true);
        if (response.requires_party) $('#party').attr('data-required', true);
        /* TODO Handle Help Text
        */
        /* Handle ID Validation Requirements
        */
        minLength = response.id_min_length || 0;
        maxLength = response.id_max_length || 100;
        $('#id_number').attr('data-maxlength', maxLength).attr('data-minlength', minLength);
        /* Handle SOS Contact Info
        */
        /* Callback to advance form
        */
        return showRegistrationForm();
      },
      error: function(error) {
        /* Handle Error
        */
      }
    });
  };

}).call(this);
