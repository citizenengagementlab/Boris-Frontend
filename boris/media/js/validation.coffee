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
	return true

validateRecentlyMoved = ($input) ->
	if $input.attr("checked") == "checked"
		### Validate Previous Address ###
		if !validateAddress $('#prev_address')
			return false
		if !validateState $('#prev_state')
			return false
		if !validateCity $('#prev_city')
			return false
		if !validateZip $('#prev_zip_code')
			return false
	return true
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
	return true

validateIDNumber = ($input) ->
	if ($input.val().toUpperCase() == "NONE" )
		return true
	maxLength = $input.attr("data-maxlength")
	minLength = $input.attr("data-minlength")
	idLength = $input.val().length
	if (idLength == 4 && !isNaN(parseFloat($input.val())) && isFinite($input.val()))
		#probably last 4 digits of social
		return true
	else if (minLength < idLength && idLength < maxLength)
		return true
	else
		return false

validateBirthday = ($input) ->
	bday = $input.val()
	if !bday
		return false
	else
		if !bday.match(/^(0[1-9]|1[012])[- \/.](0[1-9]|[12][0-9]|3[01])[- \/.](19|20)\d\d+$/)
			return false
		today    = new Date()
		birthday = new Date(bday)
		age      = today.getFullYear() - birthday.getFullYear()
		m        = today.getMonth() - birthday.getMonth()

		if (m < 0 || (m == 0 && today.getDate() < birthday.getDate()))
			age--

		if age < 17
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

validatePhoneType = ($input) ->
	#required only if phone is filled in
	if $('#phone').val() == ""
		required = false
	else
		required = true
	if (required == true && $input.val().length = 0)
		return false
	else
		return true


validateRace = ($input) ->
	required = $input.attr("data-required")
	if (required == true && $input.val().length = 0)
		return false
	else
		return true

validateParty = ($input) ->
	required = $input.attr("data-required")
	if (required == true && $input.val().length = 0)
		return false
	else
		return true

validateCitizenship = ($input) ->
	if $input.attr("checked") != "checked"
		return false
	else
		return true

validateFieldset = (fields) -> # Takes an {} of required fields
	errors = []

	for key, field of fields
		if !field.validate()
			errors.push({id: field.id, msg: field.msg})

	# Return if there is an error
	if errors.length > 0
		# Handle Validation Errors
		for error in errors
			#console.log(error.msg)
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
	clearValidationErrors($("#get_started"))
	requiredFields = {
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
	clearValidationErrors($("#personal"))

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
	clearValidationErrors($("#contact"))
	requiredFields = {
		email:
			id: "#email_address"
			msg: "Please enter a valid email address"
			validate: -> validateEmail($(@.id))
		phone:
			id: "#phone"
			msg: "Please enter a valid phone number"
			validate: -> validatePhoneNumber($(@.id))
		phone_type:
			id: "#phone_type"
			msg: "Please select a phone number type"
			validate: -> validatePhoneType($(@.id))
		}
	validateFieldset(requiredFields)

validateAdditional = ->
	clearValidationErrors($("#additional"))

	requiredFields = {
		citizen:
			id: "#us_citizen"
			msg: "You must be a U.S. citizen to register to vote"
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
	clearValidationErrors($("#address"))

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
			id: "#has_mailing_address"
			msg: "Please enter your mailing address information"
			validate: -> validateMailingAddress($(@.id))
		prevAddress:
			id: "#change_of_address"
			msg: "Please enter your previous address information"
			validate: -> validateRecentlyMoved($(@.id))
		}

	validateFieldset(requiredFields)
