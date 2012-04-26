// Generated by CoffeeScript 1.3.1
var accordionNext, accordionPrev, accordionValidate, clearValidationErrors, getCityState, getStateRequirements, initAccordion, initForm, initPage, initTabs, saveProgress, saveRegistrant, showRegistrationForm, submitRegistrationForm, submitStartForm, tabNext, tabPrev, tabValidate, validateAdditional, validateAddress, validateAddresses, validateBirthday, validateChangedName, validateCitizenship, validateCity, validateContact, validateEmail, validateFieldset, validateIDNumber, validateMailingAddress, validateName, validateParty, validatePersonal, validatePhoneNumber, validatePhoneType, validateRace, validateRecentlyMoved, validateStartFields, validateState, validateTitle, validateZip;

clearValidationErrors = function($fieldset) {
  $fieldset.find('input, textarea, select').removeClass('error');
  return $fieldset.find('p.error-message').remove();
};

validateAddress = function($input) {
  return $input.val().length > 0;
};

validateZip = function($input) {
  return $input.val().length === 5;
};

validateCity = function($input) {
  return $input.val().length > 0;
};

validateState = function($input) {
  return $input.val().length > 0;
};

validateMailingAddress = function($input) {
  if ($input.attr("checked") === "checked") {
    /* Validate Mailing Address
    */

    if (!validateAddress($('#mailing_address'))) {
      return false;
    }
    if (!validateState($('#mailing_state'))) {
      return false;
    }
    if (!validateCity($('#mailing_city'))) {
      return false;
    }
    if (!validateZip($('#mailing_zip_code'))) {
      return false;
    }
  } else {
    return true;
  }
};

validateRecentlyMoved = function($input) {
  if ($input.attr("checked") === "checked") {
    /* Validate Previous Address
    */

    if (!validateAddress($('#prev_address'))) {
      return false;
    }
    if (!validateState($('#prev_state'))) {
      return false;
    }
    if (!validateCity($('#prev_city'))) {
      return false;
    }
    if (!validateZip($('#prev_zip_code'))) {
      return false;
    }
  } else {
    return true;
  }
};

validateTitle = function($input) {
  return $input.val().length > 0;
};

validateName = function($input) {
  return $input.val().length > 0;
};

validateChangedName = function($input) {
  if ($input.attr("checked") === "checked") {
    /* Validate Previous Name
    */

    if (!validateTitle($('#prev_name_title'))) {
      return false;
    }
    if (!validateName($('#prev_first_name'))) {
      return false;
    }
    if (!validateName($('#prev_last_name'))) {
      return false;
    }
  } else {
    return true;
  }
};

validateIDNumber = function($input) {
  var idLength, maxLength, minLength;
  if ($input.val().toUpperCase() === "NONE") {
    return true;
  }
  maxLength = $input.attr("data-maxlength");
  minLength = $input.attr("data-minlength");
  idLength = $input.val().length;
  if (idLength === 4 && !isNaN(parseFloat($input.val())) && isFinite($input.val())) {
    return true;
  } else if (minLength < idLength && idLength < maxLength) {
    return true;
  } else {
    return false;
  }
};

validateBirthday = function($input) {
  var age, birthday, m, today;
  if (!$input.val()) {
    return false;
  } else {
    today = new Date();
    birthday = new Date($input.val());
    age = today.getFullYear() - birthday.getFullYear();
    m = today.getMonth() - birthday.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthday.getDate())) {
      age--;
    }
    if (age < 18) {
      return false;
    } else {
      return true;
    }
  }
};

validateEmail = function($input) {
  var re;
  re = /^(([^<>()\[\]\\.,;:\s@\"]+(\.[^<>()\[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test($input.val());
};

validatePhoneNumber = function($input) {
  var re;
  if ($input.attr('data-required') === true || $input.val().length > 0) {
    re = /(1-)?[(]*(\d{3})[) -.]*(\d{3})[ -.]*(\d{4})\D*/;
    return re.test($input.val());
  } else {
    return true;
  }
};

validatePhoneType = function($input) {
  var required;
  if ($('#phone').val() === "") {
    required = false;
  } else {
    required = true;
  }
  if (required === true && ($input.val().length = 0)) {
    return false;
  } else {
    return true;
  }
};

validateRace = function($input) {
  var required;
  required = $input.attr("data-required");
  if (required === true && ($input.val().length = 0)) {
    return false;
  } else {
    return true;
  }
};

validateParty = function($input) {
  var required;
  required = $input.attr("data-required");
  if (required === true && ($input.val().length = 0)) {
    return false;
  } else {
    return true;
  }
};

validateCitizenship = function($input) {
  if ($input.attr("checked") !== "checked") {
    return false;
  } else {
    return true;
  }
};

validateFieldset = function(fields) {
  var error, errors, field, key, _i, _len;
  errors = [];
  for (key in fields) {
    field = fields[key];
    if (!field.validate()) {
      errors.push({
        id: field.id,
        msg: field.msg
      });
    }
  }
  if (errors.length > 0) {
    for (_i = 0, _len = errors.length; _i < _len; _i++) {
      error = errors[_i];
      $(error.id).addClass('error').parent().append("<p class='error-message'>" + error.msg + "</p>").children('.error-message').hide().fadeIn();
    }
    return false;
  } else {
    return true;
  }
};

validateStartFields = function() {
  var requiredFields;
  clearValidationErrors($("#get_started"));
  requiredFields = {
    email: {
      id: "#pre_email_address",
      msg: "Please enter a valid email address",
      validate: function() {
        return validateEmail($(this.id));
      }
    },
    zip: {
      id: "#pre_zip_code",
      msg: "Please enter a 5 digit zip code",
      validate: function() {
        return validateZip($(this.id));
      }
    }
  };
  return validateFieldset(requiredFields);
};

validatePersonal = function() {
  var requiredFields;
  clearValidationErrors($("#personal"));
  requiredFields = {
    title: {
      id: "#name_title",
      msg: "Title is required",
      validate: function() {
        return validateTitle($(this.id));
      }
    },
    firstName: {
      id: "#first_name",
      msg: "First name is required",
      validate: function() {
        return validateName($(this.id));
      }
    },
    lastName: {
      id: "#last_name",
      msg: "Last name is required",
      validate: function() {
        return validateName($(this.id));
      }
    },
    nameChange: {
      id: "#change_of_name",
      msg: "Please enter your previous name",
      validate: function() {
        return validateChangedName($(this.id));
      }
    },
    idNumber: {
      id: "#id_number",
      msg: "Please enter a valid id number",
      validate: function() {
        return validateIDNumber($(this.id));
      }
    },
    birthday: {
      id: "#date_of_birth",
      msg: "Please enter a valid date in a MM/DD/YYYY format, you must be 18 years old to register.",
      validate: function() {
        return validateBirthday($(this.id));
      }
    }
  };
  return validateFieldset(requiredFields);
};

validateContact = function() {
  var requiredFields;
  clearValidationErrors($("#contact"));
  requiredFields = {
    email: {
      id: "#email_address",
      msg: "Please enter a valid email address",
      validate: function() {
        return validateEmail($(this.id));
      }
    },
    phone: {
      id: "#phone",
      msg: "Please enter a valid phone number",
      validate: function() {
        return validatePhoneNumber($(this.id));
      }
    },
    phone_type: {
      id: "#phone_type",
      msg: "Please select a phone number type",
      validate: function() {
        return validatePhoneType($(this.id));
      }
    }
  };
  return validateFieldset(requiredFields);
};

validateAdditional = function() {
  var requiredFields;
  clearValidationErrors($("#additional"));
  requiredFields = {
    citizen: {
      id: "#us_citizen",
      msg: "You must be a U.S. citizen to register to vote",
      validate: function() {
        return validateCitizenship($(this.id));
      }
    },
    race: {
      id: "#race",
      msg: "Required",
      validate: function() {
        return validateRace($(this.id));
      }
    },
    party: {
      id: "#party",
      msg: "Required",
      validate: function() {
        return validateParty($(this.id));
      }
    }
  };
  return validateFieldset(requiredFields);
};

validateAddresses = function() {
  var requiredFields;
  clearValidationErrors($("#address"));
  requiredFields = {
    home_address: {
      id: "#home_address",
      msg: "Address is required",
      validate: function() {
        return validateAddress($(this.id));
      }
    },
    city: {
      id: "#home_city",
      msg: "City is required",
      validate: function() {
        return validateCity($(this.id));
      }
    },
    state: {
      id: "#home_state_id",
      msg: "State is required",
      validate: function() {
        return validateState($(this.id));
      }
    },
    zip: {
      id: "#home_zip_code",
      msg: "Please enter a 5 digit zip code",
      validate: function() {
        return validateZip($(this.id));
      }
    },
    mailingAddress: {
      id: "#has_different_address",
      msg: "Please enter your mailing address information",
      validate: function() {
        return validateMailingAddress($(this.id));
      }
    },
    prevAddress: {
      id: "#change_of_address",
      msg: "Please enter your previous address information",
      validate: function() {
        return validateRecentlyMoved($(this.id));
      }
    }
  };
  return validateFieldset(requiredFields);
};

/* -------------------------------------------- 
     Begin staterequirements.coffee 
--------------------------------------------
*/


showRegistrationForm = function() {
  var email, firstName, lastName, zip;
  firstName = $('#pre_first_name').val();
  lastName = $('#pre_last_name').val();
  email = $('#pre_email_address').val();
  zip = $('#pre_zip_code').val();
  $('#first_name').val(firstName);
  $('#last_name').val(lastName);
  $('#email_address').val(email);
  $('#home_zip_code').val(zip);
  switch (window.LAYOUT) {
    case "singlepage":
      $('#state_form').hide();
      return $('#registration_form').show();
    case "tabs":
      $("#get_started").hide();
      $("#address").show();
      $("#get_started-tab").addClass("complete").removeClass("active");
      return $("#address-tab").addClass("active");
    case "accordion":
      $("#get_started > ul").slideUp();
      return $("#address > ul").slideDown();
  }
};

getCityState = function(zip) {
  return $.ajax({
    type: 'get',
    url: '/usps/zip_lookup/',
    data: {
      zip: zip
    },
    success: function(d) {
      /* Handle City and State Data
      */

      var homeCity, homeState;
      if (d.state !== void 0) {
        homeCity = d.city;
        homeState = d.state;
        $("#home_city").val(homeCity);
        $("#home_state_id").val(homeState).attr('readonly', 'readonly');
      }
      getStateRequirements();
      return true;
    },
    error: function(xhr, status, error) {
      /* Handle Error
      */
      $('#pre_zip_code').addClass('error').parent().append("<p class='error-message'>Invalid zip code</p>").children('.error-message').hide().fadeIn();
      $('form#get_started img.spinner').remove();
      return false;
    }
  });
};

getStateRequirements = function() {
  var data, url;
  url = "/rtv/api/v1/state_requirements.json";
  data = {
    'home_zip_code': $('#pre_zip_code').val(),
    'lang': $('#lang_id').val()
  };
  return $.ajax({
    url: url,
    data: data,
    type: 'get',
    success: function(response) {
      /* Handle Political Parties
      */

      var $target, html, maxLength, minLength, parties, party, _i, _len;
      if (response.party_list) {
        parties = response.party_list;
        $target = $('select#party');
        html = "";
        for (_i = 0, _len = parties.length; _i < _len; _i++) {
          party = parties[_i];
          /* generate html
          */

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

      if (response.requires_party) {
        $('#party').attr('data-required', true);
      }
      if (response.requires_party) {
        $('#party').attr('data-required', true);
      }
      /* Handle Help Text
      */

      if (response.id_number_msg) {
        $('#tooltip_text_id_number').text(response.id_number_msg);
      }
      if (response.requires_party_msg) {
        $('#tooltip_text_party').text(response.requires_party_msg);
      }
      if (response.requires_race_msg) {
        $('#tooltip_text_race').text(response.requires_race_msg);
      }
      /* Handle ID Validation Requirements
      */

      minLength = response.id_length_min || 0;
      maxLength = response.id_length_max || 100;
      $('#id_number').attr('data-maxlength', maxLength).attr('data-minlength', minLength);
      /* TODO: Handle SOS Contact Info (where is this used?)
      */

      /* Callback to advance form
      */

      return showRegistrationForm();
    },
    error: function(xhr, status, error) {
      var response;
      $('form#get_started img.spinner').hide();
      response = $.parseJSON(xhr.responseText);
      $('#state_form').before('<div class="error-message big-error"><h1>Sorry, you are not eligible to register to vote for the following reason(s):</h1><p>' + response.error.message + '</p></div>');
      $('#state_form').hide();
      return $('#registration').hide();
    }
  });
};

/* -------------------------------------------- 
     Begin form.coffee 
--------------------------------------------
*/


/* Form Logic
*/


$.fn.serializeJSON = function() {
  var json;
  json = {};
  $.map($(this).serializeArray(), function(n, i) {
    if (n.value === "on") {
      n.value = 1;
    } else if (n.value === "off") {
      n.value = 0;
    }
    return json[n.name] = n.value;
  });
  return json;
};

submitStartForm = function() {
  var valid;
  clearValidationErrors($('#get_started'));
  valid = validateStartFields();
  if (!valid) {
    return false;
  } else {
    saveRegistrant($('form#get_started'));
    return getCityState($("#pre_zip_code").val());
  }
};

saveRegistrant = function($form) {
  var data;
  data = $form.serializeJSON();
  return $.ajax({
    type: "POST",
    url: $form.attr('action'),
    data: {
      'registrant': data
    },
    cache: false,
    error: function(response) {},
    beforeSend: function() {
      return $('form#get_started input[type=submit]').after('<img src="http://s3.amazonaws.com/register2.rockthevote.com/img/ajax-spinner.gif" class="spinner">');
    }
  });
};

submitRegistrationForm = function() {
  var v, valid, _i, _len;
  clearValidationErrors($('#registration'));
  valid = [];
  valid.push(validateAddresses());
  valid.push(validatePersonal());
  valid.push(validateContact());
  valid.push(validateAdditional());
  if ($('.error').length > 0) {
    $('html, body').scrollTop($('.error').first().offset().top);
  }
  for (_i = 0, _len = valid.length; _i < _len; _i++) {
    v = valid[_i];
    if (!v) {
      return false;
    }
  }
  return true;
};

saveProgress = function($field) {
  return $.ajax({
    type: "POST",
    url: "/registrants/save_progress/",
    data: {
      email_address: $('#email_address').val(),
      field_name: $field.attr('name'),
      field_value: $field.val()
    },
    error: function(response) {}
  });
};

initForm = function() {
  $(".mailing").hide();
  $("#previous_name").hide();
  $(".address-change").hide();
  $("#has_different_address").click(function() {
    if ($("#has_different_address").is(":checked")) {
      return $(".mailing").fadeIn();
    } else {
      return $(".mailing").fadeOut();
    }
  });
  $("#change_of_name").click(function() {
    if ($("#change_of_name").is(":checked")) {
      return $("#previous_name").fadeIn();
    } else {
      return $("#previous_name").fadeOut();
    }
  });
  $("#change_of_address").click(function() {
    if ($("#change_of_address").is(":checked")) {
      return $(".address-change").fadeIn();
    } else {
      return $(".address-change").fadeOut();
    }
  });
  $("form#registration input, form#registration select").change(function(e) {
    return saveProgress($(this));
  });
  $("form#registration").submit(function(e) {
    e.preventDefault();
    $('form#registration input[type=submit]').after('<img src="http://s3.amazonaws.com/register2.rockthevote.com/img/ajax-spinner.gif" class="spinner">');
    if (!submitRegistrationForm()) {
      $('form#registration img.spinner').remove();
      return false;
    } else {
      return $('#registration').off('submit').submit();
    }
  });
  return $("form#get_started").submit(function(e) {
    e.preventDefault();
    if (!submitStartForm()) {
      return false;
    }
  });
};

initPage = function() {
  return $("#registration_form").hide();
};

/* -------------------------------------------- 
     Begin tab-refactor.coffee 
--------------------------------------------
*/


tabNext = function(e, self) {
  var $tab;
  $tab = $("#" + ($(self).parents('fieldset').attr('id')) + "-tab");
  $('li.tab.active').removeClass("active");
  $tab.addClass("complete");
  $tab.next().addClass("active");
  return $(self).parents('fieldset').hide().next().show();
};

tabPrev = function(e, self) {
  var $tab;
  $tab = $("#" + ($(self).parents('fieldset').attr('id')) + "-tab");
  $tab.removeClass("active");
  $tab.removeClass("complete");
  $tab.prev().addClass("active");
  return $(self).parents('fieldset').hide().prev().show();
};

tabValidate = function(id) {
  switch (id) {
    case "address":
      return validateAddresses();
    case "personal":
      return validatePersonal();
    case "contact":
      return validateContact();
    case "additional":
      return validateAdditional();
    default:
      return true;
  }
};

initTabs = function() {
  var $fieldsets, counter, html;
  $fieldsets = $('fieldset');
  $fieldsets.hide().filter(':first').show();
  html = "<div id=\"tab-indicators\"><ol></ol></div>";
  $('#state_form').before(html);
  counter = 1;
  $fieldsets.each(function() {
    var $fs, tabClass;
    $fs = $(this);
    if ($fs.find('li.form-action').length !== 1) {
      $fs.children('ul').append("<li class=\"form-action\"></li>");
    }
    if ($fs.next().length !== 0) {
      $fs.find('li.form-action').append("<button class=\"btn-next\">Next</button>");
    }
    if ($fs.prev().length !== 0) {
      $fs.find('li.form-action').append("<button class=\"btn-prev\">Back</button>");
    }
    tabClass = counter === 1 ? "active tab" : "tab";
    html = "<li class=\"" + tabClass + "\" id=\"" + ($fs.attr('id')) + "-tab\">\n	Step " + counter + "\n</li>";
    $('#tab-indicators > ol').append(html);
    return counter++;
  });
  $("button.start-over").on('click', function(e) {
    e.preventDefault();
    return window.location.reload();
  });
  $("button.btn-next").on('click', function(e) {
    e.preventDefault();
    if (tabValidate($(this).parents('fieldset').attr('id')) !== true) {
      return false;
    } else {
      return tabNext(e, this);
    }
  });
  return $("button.btn-prev").on('click', function(e) {
    e.preventDefault();
    return tabPrev(e, this);
  });
};

/* -------------------------------------------- 
     Begin accordion-refactor.coffee 
--------------------------------------------
*/


accordionNext = function(e, self) {
  return $(self).parents('ul').slideUp().parent('fieldset').next().children('ul').slideDown();
};

accordionPrev = function(e, self) {
  return $(self).parents('ul').slideUp().parent('fieldset').prev().children('ul').slideDown();
};

accordionValidate = function(id) {
  switch (id) {
    case "address":
      return validateAddresses();
    case "personal":
      return validatePersonal();
    case "contact":
      return validateContact();
    case "additional":
      return validateAdditional();
    default:
      return true;
  }
};

initAccordion = function() {
  var $fieldsets;
  $fieldsets = $('fieldset > ul');
  $fieldsets.hide().filter(':first').show();
  $('#registration_form').show();
  $('legend').addClass('accordion-header');
  $fieldsets.each(function() {
    var $fs;
    $fs = $(this);
    if ($fs.find('li.form-action').length !== 1) {
      $fs.append("<li class=\"form-action\"></li>");
    }
    if ($fs.parent('fieldset').next().length !== 0) {
      $fs.find('li.form-action').append("<button class=\"btn-next\">Next</button>");
    }
    if ($fs.parent('fieldset').prev().length !== 0) {
      return $fs.find('li.form-action').append("<button class=\"btn-prev\">Back</button>");
    }
  });
  $("button.start-over").on('click', function(e) {
    e.preventDefault();
    return window.location.reload();
  });
  $("button.btn-next").on('click', function(e) {
    e.preventDefault();
    if (accordionValidate($(this).parents('fieldset').attr('id')) !== true) {
      return false;
    } else {
      return accordionNext(e, this);
    }
  });
  return $("button.btn-prev").on('click', function(e) {
    e.preventDefault();
    return accordionPrev(e, this);
  });
};

/* -------------------------------------------- 
     Begin application.coffee 
--------------------------------------------
*/


jQuery(function($) {
  initForm();
  switch (window.LAYOUT) {
    case "singlepage":
      return initPage();
    case "tabs":
      return initTabs();
    case "accordion":
      return initAccordion();
  }
});
