#@codekit-prepend 'validation.coffee'
#@codekit-prepend 'staterequirements.coffee'
#@codekit-prepend 'form.coffee'
#@codekit-prepend 'tab-refactor.coffee'
#@codekit-prepend 'accordion-refactor.coffee'

jQuery ($) ->
	initForm()
	console.log "ALL THE #{window.LAYOUT.toUpperCase()}!!!"
	switch window.LAYOUT
	  when "singlepage"
	  	initPage()
	  when "tabs"
	  	initTabs()
	  when "accordion"
	  	initAccordion()
