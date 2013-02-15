

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
$topShadow = $(".scroll-shadows.top")
$bottomShadow = $(".scroll-shadows.bottom")

check = ->

  if content.scrollHeight != content.offsetHeight
    $main.addClass('scrollable')
  else
    $main.removeClass('scrollable')
  
  if content.scrollTop == 0
    $topShadow.addClass('at-top')
  else if content.scrollHeight == content.offsetHeight + content.scrollTop
    $bottomShadow.addClass('at-bottom')
  else
    $topShadow.removeClass('at-top')
    $bottomShadow.removeClass('at-bottom')

  requestAnimFrame(check)

check()