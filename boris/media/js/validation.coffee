validateAddress = (input) ->
	return input.val().length > 0

validateZip = (input) ->
	return input.val().length == 5

validateCity = (input) ->
	return input.val().length > 0

validateState = (input) ->
	return input.val() > 0

validateMailingAddress = (input) ->
	if input.attr("checked") == "checked"
		### TODO: Validate Mailing Address ###
	else
		true

validateRecentlyMoved = (input) ->
	if input.attr("checked") == "checked"
		### TODO: Validate Previous Address ###
	else
		true

validateTitle = (input) ->
	return input.val().length > 0

validateFirstName = (input) ->
	return input.val().length > 0

validateLastName = (input) ->
	return input.val().length > 0

validateChangedName = (input) ->
	if input.attr("checked") == "checked"
		### TODO: Validate Previous Name ###
	else
		true

validateIDNumber = (input) ->
	maxLength = input.attr("data-maxlength")
	minLength = input.attr("data-minlength")
	idLength = input.val().length
	if (minLength > idLength || idLength > maxLength)
		false
	else
		true

validateBirthday = (input) ->
	today    = new Date()
	birthday = new Date(input.val())
	age      = today.getFullYear() - birthday.getFullYear()
	m        = today.getMonth() - birthday.getMonth()

	if (m < 0 || (m == 0 && today.getDate() < birthday.getDate()))
		age--

	if age < 18
		false
	else
		true

validateEmail = (input) ->
	re = /^(([^<>()\[\]\\.,;:\s@\"]+(\.[^<>()\[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
	re.test(input.val())

validatePhoneNumber = (input) ->
	re = /(1-)?[(]*(\d{3})[) -.]*(\d{3})[ -.]*(\d{4})\D*/
	re.test(input.val())

validateRace = (input) ->
	required = input.attr("data-required")
	if (required == true && input.val().length = 0)
		false
	else
		true

validateParty = (input) ->
	required = input.attr("data-required")
	if (required == true && input.val().length = 0)
		false
	else
		true

validateCitizenship = (input) ->
	if input.attr("checked") != "checked"
		false
	else
		true
