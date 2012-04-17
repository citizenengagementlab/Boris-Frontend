var validateAddress, validateBirthday, validateChangedName, validateCitizenship, validateCity, validateEmail, validateFirstName, validateIDNumber, validateLastName, validateMailingAddress, validateParty, validatePhoneNumber, validateRace, validateRecentlyMoved, validateState, validateTitle, validateZip;

validateAddress = function(input) {
  return input.val().length > 0;
};

validateZip = function(input) {
  return input.val().length === 5;
};

validateCity = function(input) {
  return input.val().length > 0;
};

validateState = function(input) {
  return input.val() > 0;
};

validateMailingAddress = function(input) {
  if (input.attr("checked") === "checked") {
    /* TODO: Validate Mailing Address
    */
  } else {
    return true;
  }
};

validateRecentlyMoved = function(input) {
  if (input.attr("checked") === "checked") {
    /* TODO: Validate Previous Address
    */
  } else {
    return true;
  }
};

validateTitle = function(input) {
  return input.val().length > 0;
};

validateFirstName = function(input) {
  return input.val().length > 0;
};

validateLastName = function(input) {
  return input.val().length > 0;
};

validateChangedName = function(input) {
  if (input.attr("checked") === "checked") {
    /* TODO: Validate Previous Name
    */
  } else {
    return true;
  }
};

validateIDNumber = function(input) {
  var idLength, maxLength, minLength;
  maxLength = input.attr("data-maxlength");
  minLength = input.attr("data-minlength");
  idLength = input.val().length;
  if (minLength > idLength || idLength > maxLength) {
    return false;
  } else {
    return true;
  }
};

validateBirthday = function(input) {
  var age, birthday, m, today;
  today = new Date();
  birthday = new Date(input.val());
  age = today.getFullYear() - birthday.getFullYear();
  m = today.getMonth() - birthday.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < birthday.getDate())) age--;
  if (age < 18) {
    return false;
  } else {
    return true;
  }
};

validateEmail = function(input) {
  var re;
  re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(input.val());
};

validatePhoneNumber = function(input) {
  var re;
  re = /(1-)?[(]*(\d{3})[) -.]*(\d{3})[ -.]*(\d{4})\D*/;
  return re.test(input.val());
};

validateRace = function(input) {
  var required;
  required = input.attr("data-required");
  if (required === true && (input.val().length = 0)) {
    return false;
  } else {
    return true;
  }
};

validateParty = function(input) {
  var required;
  required = input.attr("data-required");
  if (required === true && (input.val().length = 0)) {
    return false;
  } else {
    return true;
  }
};

validateCitizenship = function(input) {
  if (input.attr("checked") !== "checked") {
    return false;
  } else {
    return true;
  }
};
