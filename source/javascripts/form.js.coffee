

@form = form = new Views.Form
  el: $ ".registration-form"

form.focusInputByIndex 0
form.disableButton()

# Ref: http://paulirish.com/2011/requestanimationframe-for-smart-animating/
requestAnimFrame = (()->
    window.requestAnimationFrame  ||
    window.webkitRequestAnimationFrame ||
    window.mozRequestAnimationFrame    ||
    window.oRequestAnimationFrame      ||
    window.msRequestAnimationFrame     ||
    (callback) -> window.setTimeout(callback, 1000 / 60)
  )()

content = document.getElementById("content")
$main = $ "#main"

check = ->

  if content.scrollHeight != content.offsetHeight
    $main.addClass('scrollable')
  else
    $main.removeClass('scrollable')
  
  if content.scrollTop == 0
    $(".scroll-shadows.top").addClass('at-top')
  else if content.scrollHeight == content.offsetHeight + content.scrollTop
    $(".scroll-shadows.bottom").addClass('at-bottom')
  else
    $(".scroll-shadows.top").removeClass('at-top')
    $(".scroll-shadows.bottom").removeClass('at-bottom')

  requestAnimFrame(check)

check()

