clearValidationErrors = ($fieldset) ->
	$fieldset.find('input, textarea, select')
		.removeClass('error')
	$fieldset.find('p.error-message')
		.remove()

validateAddress = ($input) ->
	return $input.val().length > 0

validateZip = ($input) ->
	return $input.val().length == 5

validateCity = ($input) ->
	return $input.val().length > 0

validateState = ($input) ->
	return $input.val().length > 0

validateMailingAddress = ($input) ->
	if $input.attr("checked") == "checked"
		### Validate Mailing Address ###
		if !validateAddress $('#mailing_address')
			return false
		if !validateState $('#mailing_state')
			return false
		if !validateCity $('#mailing_city')
			return false
		if !validateZip $('#mailing_zip_code')
			return false
	else
		true

validateRecentlyMoved = ($input) ->
	if $input.attr("checked") == "checked"
		### TODO: Validate Previous Address ###
		if !validateAddress $('#prev_address')
			return false
		if !validateState $('#prev_state')
			return false
		if !validateCity $('#prev_city')
			return false
		if !validateZip $('#prev_zip_code')
			return false
	else
		true

validateTitle = ($input) ->
	return $input.val().length > 0

validateName = ($input) ->
	return $input.val().length > 0

validateChangedName = ($input) ->
	if $input.attr("checked") == "checked"
		### Validate Previous Name ###
		if !validateTitle $('#prev_name_title')
			return false
		if !validateName $('#prev_first_name')
			return false
		if !validateName $('#prev_last_name')
			return false
	else
		true

validateIDNumber = ($input) ->
	if ($input.val().toUpperCase() == "NONE" )
		return true
	maxLength = $input.attr("data-maxlength")
	minLength = $input.attr("data-minlength")
	idLength = $input.val().length
	if (minLength > idLength || idLength > maxLength)
		return false
	else
		return true

validateBirthday = ($input) ->
	if !$input.val()
		return false
	else
		today    = new Date()
		birthday = new Date($input.val())
		age      = today.getFullYear() - birthday.getFullYear()
		m        = today.getMonth() - birthday.getMonth()

		if (m < 0 || (m == 0 && today.getDate() < birthday.getDate()))
			age--

		if age < 18
			return false
		else
			return true

validateEmail = ($input) ->
	re = /^(([^<>()\[\]\\.,;:\s@\"]+(\.[^<>()\[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
	re.test($input.val())

validatePhoneNumber = ($input) ->
	if $input.attr('data-required') == true || $input.val().length > 0
		re = /(1-)?[(]*(\d{3})[) -.]*(\d{3})[ -.]*(\d{4})\D*/
		return re.test($input.val())
	else
		return true
validateRace = ($input) ->
	required = $input.attr("data-required")
	if (required == true && $input.val().length = 0)
		false
	else
		true

validateParty = ($input) ->
	required = $input.attr("data-required")
	if (required == true && $input.val().length = 0)
		false
	else
		true

validateCitizenship = ($input) ->
	if $input.attr("checked") != "checked"
		false
	else
		true

validateFieldset = (fields) -> # Takes an {} of required fields
	errors = []

	for key, field of fields
		if !field.validate()
			errors.push({id: field.id, msg: field.msg})

	# Return if there is an error
	if errors.length > 0
		# Handle Validation Errors
		for error in errors
			console.log(error.msg)
			$(error.id)
				.addClass('error')
				.parent()
				.append("<p class='error-message'>#{error.msg}</p>")
				.children('.error-message')
				.hide()
				.fadeIn()
		return false
	else
		return true

validateStartFields = ->
	requiredFields = {
		firstName:
			id: "#pre_first_name"
			msg: "First name is required"
			validate: -> validateName($(@.id))
		lastName:
			id: "#pre_last_name"
			msg: "Last name is required"
			validate: -> validateName($(@.id))
		email:
			id: "#pre_email_address"
			msg: "Please enter a valid email address"
			validate: -> validateEmail($(@.id))
		zip:
			id: "#pre_zip_code"
			msg: "Please enter a 5 digit zip code"
			validate: -> validateZip($(@.id))
		}

	validateFieldset(requiredFields)

validatePersonal = ->
	requiredFields = {
		title:
			id: "#name_title"
			msg: "Title is required"
			validate: -> validateTitle($(@.id))
		firstName:
			id: "#first_name"
			msg: "First name is required"
			validate: -> validateName($(@.id))
		lastName:
			id: "#last_name"
			msg: "Last name is required"
			validate: -> validateName($(@.id))
		nameChange:
			id: "#change_of_name"
			msg: "Please enter your previous name"
			validate: -> validateChangedName($(@.id))
		idNumber:
			id: "#id_number"
			msg: "Please enter a valid id number"
			validate: -> validateIDNumber($(@.id))
		birthday:
			id: "#date_of_birth"
			msg: "Please enter a valid date in a MM/DD/YYYY format, you must be 18 years old to register."
			validate: -> validateBirthday($(@.id))
		}

	validateFieldset(requiredFields)

validateContact = ->
	requiredFields = {
		email:
			id: "#email_address"
			msg: "Please enter a valid email address"
			validate: -> validateEmail($(@.id))
		phone:
			id: "#phone"
			msg: "Please enter a valid phone number"
			validate: -> validatePhoneNumber($(@.id))	
		}
	validateFieldset(requiredFields)

validateAdditional = ->
	requiredFields = {
		citizen:
			id: "#us_citizen"
			msg: "You must be a US citizen"
			validate: -> validateCitizenship($(@.id))
		race:
			id: "#race"
			msg: "Required"
			validate: -> validateRace($(@.id))
		party:
			id: "#party"
			msg: "Required"
			validate: -> validateParty($(@.id))
		}

	validateFieldset(requiredFields)

validateAddresses = ->
	requiredFields = {
		home_address:
			id: "#home_address"
			msg: "Address is required"
			validate: -> validateAddress($(@.id))
		city:
			id: "#home_city"
			msg: "City is required"
			validate: -> validateCity($(@.id))
		state:
			id: "#home_state_id"
			msg: "State is required"
			validate: -> validateState($(@.id))
		zip:
			id: "#home_zip_code"
			msg: "Please enter a 5 digit zip code"
			validate: -> validateZip($(@.id))
		mailingAddress:
			id: "#has_different_address"
			msg: "Please enter your mailing address information"
			validate: -> validateMailingAddress($(@.id))
		prevAddress:
			id: "#change_of_address"
			msg: "Please enter your previous address information"
			validate: -> validateRecentlyMoved($(@.id))
		}

	validateFieldset(requiredFields)
