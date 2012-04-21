### Form Logic ###

$.fn.serializeJSON = ->
	json = {}
	$.map($(@).serializeArray(), (n, i) ->
			if n.value == "on"
				n.value = 1
			else if n.value == "off"
				n.value = 0
			json[n.name] = n.value
		)
	json

clearValidationErrors = ($form) ->
	$form.find('input, textarea, select')
		.removeClass('error')
	$form.find('p.error-message')
		.remove()

submitStartForm = ->
	clearValidationErrors($('#get_started'))

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

	errors = []

	for key, field of requiredFields
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
				.children('label')
				.append("<p class='error-message'>#{error.msg}</p>")
				.children('.error-message')
				.hide()
				.fadeIn()
		return false
	else
		getCityState($("#pre_zip_code").val())
		saveRegistrant($('form#get_started'))
		
saveRegistrant = ->
	data = $(@).serializeJSON()
	$.ajax({
		type: "POST"
		url: $(@).attr('action')
		data: {'registrant':data}
		cache: false
		error: (response) -> #handle error
			console.log response
	})
	

submitRegistrationForm = ->
	clearValidationErrors($('#registration'))
	
	# validate registration form inputs
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

	for key, field of requiredFields
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
				.children('label')
				.append("<p class='error-message'>#{error.msg}</p>")
				.children('.error-message')
				.hide()
				.fadeIn()
		return false
	else
		# Post registration
		data = $(@).serializeJSON()

		requiredBools = [
			'opt_in_email'
			'opt_in_sms'
			'us_citizen'
		]

		for i in requiredBools
			if !data[requiredBools[i]]
				data[requiredBools[i]] = 0

		console.log 'Ready to Send:'
		console.log data
		
		return true

saveProgress = ($field) ->
	console.log($field)
	$.ajax({
		type:"POST"
		url: "/registrants/save_progress/"
		data: {
			email_address:$('#email_address').val()
			field_name:$field.attr('name')
			field_value:$field.val()
		}
		error: (response) ->
			console.log(response);
	})

initForm = ->
	# Setup Hidden Elements
	$("#registration_form").hide()	
	$(".mailing").hide()
	$(".name-change").hide()
	$(".address-change").hide()
	# Setup click handlers
	$("#has_different_address").click ->
	  if $("#has_different_address").is(":checked")
	    $(".mailing").fadeIn()
	  else
	    $(".mailing").fadeOut()

	$("#change_of_name").click ->
	  if $("#change_of_name").is(":checked")
	    $(".name-change").fadeIn()
	  else
	    $(".name-change").fadeOut()

	$("#change_of_address").click ->
	  if $("#change_of_address").is(":checked")
	    $(".address-change").fadeIn()
	  else
	    $(".address-change").fadeOut()

	# Setup Form Submit Events
	$("form#get_started").submit(
		(e) ->
			e.preventDefault()
			if !submitStartForm()
				return false
		)
	$("form#registration").submit(
		(e) ->
			e.preventDefault()
			if !submitRegistrationForm()
				return false
		)
	$("form#registration input, form#registration select").change(
		(e) ->
			saveProgress($(@))
	)


	# TODO: Setup Onchange Validation Logic
