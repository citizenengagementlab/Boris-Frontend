### Form Logic ###

submitStartForm = ->
	# validate start form inputs
	$firstname = $("#pre_first_name")
	$lastname  = $("#pre_last_name")
	$email     = $("#pre_email_address")
	$zip       = $("#pre_zip_code")

	errors = []

	if !validateFirstName($firstname)
		errors.push({id: $firstname.attr('id'), msg: "First Name is Required"})
	if !validateLastName($lastname)
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
	$title          = $("#name_title")
	$firstname      = $("#first_name")
	$lastname       = $("#last_name")
	$namechange     = $("#change_of_name")
	$idnumber       = $("#id_number")
	$dob            = $("#date_of_birth")
	$email          = $("#email_address")
	$phone          = $("#phone")
	$address        = $("#home_address")
	$city           = $("#home_city")
	$state          = $("#home_state_id")
	$zip            = $("#zip_code")
	$mailingaddress = $("#has_different_address")
	$prevaddress    = $("#change_of_address")

	errors = []

	if !validateTitle($title)
		errors.push({id: $title.attr('id'), msg: "Title is Required"})
	if !validateFirstName($firstname)
		errors.push({id: $firstname.attr('id'), msg: "First Name is Required"})
	if !validateLastName($lastname)
		errors.push({id: $lastname.attr('id'), msg: "Last Name is Required"})
	if !validateEmail($email)
		errors.push({id: $email.attr('id'), msg: "Enter a Valid Email Address"})
	if !validateZip($zip)
		errors.push({id: $zip.attr('id'), msg: "Please Enter a Valid Zip Code"})
	if !validateChangedName($namechange)
		errors.push({id: $namechange.attr('id'), msg: "Please include your previous name"})
	if !validateIDNumber($idnumber)
		errors.push({id: $idnumber.attr('id'), msg: "Please enter a valid ID Number"})
	if !validateBirthday($dob)
		errors.push({id: $dob.attr('id'), msg: "Please enter a valid date in a MM/DD/YYYY format, you must be 18 years old to register"})
	if !validatePhoneNumber($phone)
		errors.push({id: $phone.attr('id'), msg: "Enter a valid phone number"})
	if !validateAddress($address)
		errors.push({id: $address.attr('id'), msg: "Address is Required"})
	if !validateCity($city)
		errors.push({id: $city.attr('id'), msg: "City is Required"})
	if !validateState($state)
		errors.push({id: $state.attr('id'), msg: "State is Required"})
	if !validateMailingAddress($mailingaddress)
		errors.push({id: $mailingaddress.attr('id'), msg: "Please enter your mailing address"})
	if !validateRecentlyMoved($prevaddress)
		errors.push({id: $prevaddress.attr('id'), msg: "Please enter your previous address information"})

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


	# TODO: Setup Validation Logic