fsNext = (e, self) ->
	$(self)
		.parents('ul')
		.slideUp()
		.parent('fieldset')
		.next()
		.children('ul')
		.slideDown()

fsPrev = (e, self) ->
		$(self)
		.parents('ul')
		.slideUp()
		.parent('fieldset')
		.prev()
		.children('ul')
		.slideDown()

fsValidate = (id) ->
		switch id
			when "address"
				return validateAddresses()
			when "personal"
				return validatePersonal()
			when "contact"
				return validateContact()
			when "additional"
				return validateAdditional()
			else
				return true

initAccordion = ->
	# Hide unused fieldsets
	$fieldsets = $('fieldset > ul')
	$fieldsets.hide()
		.filter(':first')
		.show()
	$('#registration_form').show()
	$('legend').addClass('accordion-header')
	$fieldsets.each ->
		$fs = $(this)
		unless $fs.find('li.form-action').length == 1
			$fs.append("<li class=\"form-action\"></li>")
		unless $fs.parent('fieldset').next().length == 0
			$fs.find('li.form-action').prepend("<button class=\"btn-next\">Next</button>")
		unless $fs.parent('fieldset').prev().length == 0
			$fs.find('li.form-action').prepend("<button class=\"btn-prev\">Back</button>")

	# Bind Click Handlers
	$("button.btn-next").on('click', (e) ->
		e.preventDefault()
		if fsValidate($(this).parents('fieldset').attr('id')) != true
			false
		else
			fsNext(e, this)
	)
	$("button.btn-prev").on('click', (e) ->
		e.preventDefault()
		console.log "Next!"
		fsPrev(e, this)
	)