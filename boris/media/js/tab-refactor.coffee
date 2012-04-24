tabNext = (e, self) ->
	$(self)
		.parents('fieldset')
		.hide()
		.next()
		.show()

tabPrev = (e, self) ->
		$(self)
		.parents('fieldset')
		.hide()
		.prev()
		.show()

tabValidate = (id) ->
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

initTabs = ->
	# Hide unused fieldsets
	$fieldsets = $('fieldset')
	$fieldsets.hide()
		.filter(':first')
		.show()

	# Generate Fieldset Header
	html = "<div id=\"tab-indicators\"><ol></ol></div>"
	$('#state_form').before(html)

	$fieldsets.each ->
		$fs = $(this)
		unless $fs.find('li.form-action').length == 1
			$fs.children('ul').append("<li class=\"form-action\"></li>")
		unless $fs.next().length == 0
			$fs.find('li.form-action').append("<button class=\"btn-next\">Next</button>")
		unless $fs.prev().length == 0
			$fs.find('li.form-action').append("<button class=\"btn-prev\">Back</button>")
		text = $fs.children('legend').text()
		
		html = """
				<li>
					<a href=\"##{ $fs.attr('id') }\">#{text}</a>
				</li>
				"""
		$('#tab-indicators > ol').append(html)

	# Bind Click Handlers
	$("button.btn-next").on('click', (e) ->
		e.preventDefault()
		if tabValidate($(this).parents('fieldset').attr('id')) != true
			false
		else
			tabNext(e, this)
	)
	$("button.btn-prev").on('click', (e) ->
		e.preventDefault()
		console.log "Next!"
		tabPrev(e, this)
	)