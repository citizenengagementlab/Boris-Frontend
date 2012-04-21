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
	maxLength = $input.attr("data-maxlength")
	minLength = $input.attr("data-minlength")
	idLength = $input.val().length
	if (minLength > idLength || idLength > maxLength)
		false
	else
		true

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