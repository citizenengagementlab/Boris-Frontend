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

submitStartForm = ->
	clearValidationErrors($('#get_started'))
	valid = validateStartFields()
	if !valid
		return false
	else
		saveRegistrant($('form#get_started'))
		getCityState($("#pre_zip_code").val())
		
saveRegistrant = ($form) ->
	data = $form.serializeJSON()
	#console.log data
	$.ajax({
		type: "POST"
		url: $form.attr('action')
		data: {'registrant':data}
		cache: false
		error: (response) -> #handle error
			#console.log response
		beforeSend: ->
			#show spinner
			$('form#get_started input[type=submit]')
				.after('<img src="http://s3.amazonaws.com/register2.rockthevote.com/img/ajax-spinner.gif" class="spinner">')
	})
	

submitRegistrationForm = ->
	clearValidationErrors($('#registration'))
	valid = []
	valid.push validateAddresses()
	valid.push validatePersonal()
	valid.push validateContact()
	valid.push validateAdditional()
	if $('.error').length > 0
		$('html, body').scrollTop( $('.error').first().offset().top )

	for v in valid
		if !v
			return false
	return true

saveProgress = ($field) ->
	$.ajax({
		type:"POST"
		url: "/registrants/save_progress/"
		data: {
			email_address:$('#email_address').val()
			field_name:$field.attr('name')
			field_value:$field.val()
		}
		error: (response) ->
			#console.log(response);
	})

initForm = ->
	# Setup Hidden Elements
	$(".mailing").hide()
	$("#previous_name").hide()
	$(".address-change").hide()

	# Setup click handlers
	$("#has_different_address").click ->
	  if $("#has_different_address").is(":checked")
	    $(".mailing").fadeIn()
	  else
	    $(".mailing").fadeOut()

	$("#change_of_name").click ->
	  if $("#change_of_name").is(":checked")
	    $("#previous_name").fadeIn()
	  else
	    $("#previous_name").fadeOut()

	$("#change_of_address").click ->
	  if $("#change_of_address").is(":checked")
	    $(".address-change").fadeIn()
	  else
	    $(".address-change").fadeOut()
	$("form#registration input, form#registration select").change(
		(e) ->
			saveProgress($(@))
	)
	$("form#registration").submit(
		(e) ->
			e.preventDefault()
			$('form#registration input[type=submit]')
				.after('<img src="http://s3.amazonaws.com/register2.rockthevote.com/img/ajax-spinner.gif" class="spinner">')
			if !submitRegistrationForm()
				$('form#registration img.spinner').remove()
				return false
			else
				$('#registration')
					.off('submit')
					.submit()
		)
	$("#pre_zip_code, #home_zip_code").on('change', (e) ->
			updateCityState($(this))
		)
	# Setup Form Submit Events
	$("form#get_started").submit(
		(e) ->
			e.preventDefault()
			if !submitStartForm()
				return false
		)

initPage = ->
	# Hide Registration Form
	$("#registration_form").hide()
	$("legend").addClass('visuallyhidden')
		.filter(".visible")
		.removeClass('visuallyhidden')
	