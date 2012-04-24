tabsInit = ->
	# Hide unused fieldsets
	$fieldsets = $('fieldset')
	$fieldsets.hide()
		.filter(':first')
		.addClass('active')
		.show()
	# TODO: Generate Fieldset Header
	headerHTML = "<ol>\n"
	$fieldsets.each ->
		$fs = $(this)
		text = $fs.children('legend').text()
		headerHTML += "<li>#{text}</li>\n"
	headerHTML += "</ol>"

	# TODO: Next and Previous Functions
		# Hide current tabs
		# Show next/previous tab
	# TODO: Append Buttons
	# TODO: Click handlers
