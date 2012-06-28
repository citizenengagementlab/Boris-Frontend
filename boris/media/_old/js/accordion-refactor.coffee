accordionNext = (e, self) ->
	$(self)
		.parents('ul')
		.slideUp()
		.parent('fieldset')
		.next()
		.children('ul')
		.slideDown()

accordionPrev = (e, self) ->
		$(self)
		.parents('ul')
		.slideUp()
		.parent('fieldset')
		.prev()
		.children('ul')
		.slideDown()

accordionValidate = (id) ->
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
	$('legend:not(.visible)').addClass('accordion-header') #Don't add class to optional fieldsets#
	$fieldsets.each ->
		$fs = $(this)
		unless $fs.find('li.form-action').length == 1
			$fs.append("<li class=\"form-action\"></li>")
		unless $fs.parent('fieldset').next().length == 0
			$fs.find('li.form-action').append("<button class=\"btn-next\">Next</button>")
		unless $fs.parent('fieldset').prev().length == 0
			$fs.find('li.form-action').append("<button class=\"btn-prev\">Back</button>")
	# Start Over button
	# $("fieldset#address").find("li.form-action").append("<button class=\"start-over\">Go Back</button>")

	# Bind Click Handlers
	$("button.start-over").on('click',(e) ->
  		e.preventDefault()
  		window.location.reload();
  	)

	$("button.btn-next").on('click', (e) ->
		e.preventDefault()
		if accordionValidate($(this).parents('fieldset').attr('id')) != true
			false
		else
			accordionNext(e, this)
	)
	$("button.btn-prev").on('click', (e) ->
		e.preventDefault()
		#console.log "Next!"
		accordionPrev(e, this)
	)