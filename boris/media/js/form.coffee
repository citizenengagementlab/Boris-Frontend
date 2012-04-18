### Form Logic ###

submitStartForm = ->
	
	getCityState($("#pre_zip_code").val())


initForm = ->
	# Setup Hidden Elements
	$("#registration_form").hide()	
	$(".mailing").hide()
	$(".name-change").hide()
	$(".address-change").hide()

	# Setup AJAX Calls
	$("form#get_started")
		.submit(
			(e) ->
				e.preventDefault()
				submitStartForm()
		)

	# TODO: Setup Validation Logic