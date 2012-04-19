### Form Logic ###

submitStartForm = ->
	# validate start form inputs
	$firstname = $("#pre_first_name")
	$lastname  = $("#pre_last_name")
	$email     = $("#pre_email_address")
	$zip       = $("#pre_zip_code")

	errors = []

	if !validateName($firstname)
		errors.push({id: $firstname.attr('id'), msg: "First Name is Required"})
	if !validateName($lastname)
		errors.push({id: $lastname.attr('id'), msg: "Last Name is Required"})
	if !validateEmail($email)
		errors.push({id: $email.attr('id'), msg: "Enter a Valid Email Address"})
	if !validateZip($zip)
		errors.push({id: $zip.attr('id'), msg: "Please Enter a Valid Zip Code"})

	# Return if there is an error
	if errors.length < 0
		# Handle Validation Errors
		for i in errors
			$(errors[i].id)
				.addClass('error')
				.prepend("<span class='error-message'>#{errors[i].msg}</span>")
		return false
	else
		getCityState($("#pre_zip_code").val())

submitRegistrationForm = ->
	# validate registration form inputs
	fields = {
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
		email:
			id: "#email_address"
			msg: "Please enter a valid email address"
			validate: -> validateEmail($(@.id))
		phone:
			id: "#phone"
			msg: "Please enter a valid phone number"
			validate: -> validatePhoneNumber($(@.id))
		address:
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
			id: "#zip_code"
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

	errors = []

	for field in fields
		if field.validate
			continue
		else
			errors.push({id: field.id, msg: field.msg})

	# Return if there is an error
	if errors.length < 0
		# Handle Validation Errors
		for i in errors
			$(errors[i].id)
				.addClass('error')
				.prepend("<span class='error-message'>#{errors[i].msg}</span>")
		return false
	else
		getCityState($("#pre_zip_code").val())

initForm = ->
	# Setup Hidden Elements
	$("#registration_form").hide()	
	$(".mailing").hide()
	$(".name-change").hide()
	$(".address-change").hide()

	# Setup Form Submit Events
	$("form#get_started").submit(
		(e) ->
			e.preventDefault()
			submitStartForm()
		)
	$("registration").submit(
		(e) ->
			e.preventDefault()
			submitRegistrationForm()
		)

	# TODO: Setup Onchange Validation Logic
