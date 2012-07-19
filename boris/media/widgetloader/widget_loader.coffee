$ ->
  $('a.ovr-close').live 'click', (e) ->
    e.preventDefault()
    close = confirm("Are you sure you want to close the voter registration form?")
    if close
      $('.ovr-overlay, #ovr-container').remove()
    else
      return false
  
  registrationLinks = $ 'a.floatbox[href*="rockthevote.com/registrants/new"]'
  registrationLinks.on 'click', (e) ->
    e.preventDefault()
    $el = $(@)
    $body = $('body')
    $overlay = $ '<div class="ovr-overlay" />'
    $iframe  = $ '<iframe id="ovr-widget" />'
    $close = $ '<a href="#" class="ovr-close">close [x]</a>'
    $container = $ '<div id="ovr-container" />'
    $iframe.attr('src', $el.attr('href'))
    $body.append $container
    $container.append $overlay
    $overlay.hide().fadeIn(300)
    $container.append $iframe
    $container.prepend($close)
