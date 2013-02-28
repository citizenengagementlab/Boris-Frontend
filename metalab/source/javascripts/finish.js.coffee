class Ellipsis extends Backbone.View
  tagName: "span"
  className: "Ellipsis"
  states: [ '', '.', '..', '...' ]
  
  initialize: ($el) ->
    @$el = $el
    @run = true
    @count = 0
    @play()

  render: ->
    @$el.text @states[@count % 4]

  play: =>
    @count += 1
    @render()
    if @run
      setTimeout(@play, 500)

  stop: =>
    @run = false

checkPdfUrl = ->
  downloadLink = $('a.download').attr('href')
  a = $('<a />')
  a.href = downloadLink
  proxyUrl = a.pathname
  $.ajax
    url: proxyUrl
    type: "HEAD"
    cache: false
    error: (xhr, status, err) ->
      setTimeout checkPdfUrl, 1000 unless status == "Unknown" # Gross I.E. 8 hack, doesn't return a proper statuscode from the AJAX request 
      if status == "Unknown"
        setTimeout ->
          $('#waiting').hide()
          $('#download').show()
        , 2000 # Just wait 2 seconds and fade it in!

    success: (d) ->
      window.ellipsis.stop()
      $('#waiting').fadeOut( ->
        $('#download').fadeIn()
      )


$ ->
  $('#download').hide()
  window.ellipsis = new Ellipsis $('span.ellipsis')
  setTimeout checkPdfUrl, 3000
