

$ ->
  $(":checkbox").each ->
    $el = $ this
    $fake = $ "<div class='fake-checkbox'></div>"

    $el.wrap "<div class='fake-checkbox-wrap'></div>"
    $el.parent().append($fake)

    check = ->
      $fake.toggleClass("checked", $el.prop("checked"))
      $fake.toggleClass("focus", document.activeElement == this)

    $el.on("change blur focus keyup", check)




@form = form = new Views.Form
  el: $ ".registration-form"

form.focusInputByIndex 0
form.disableButton()
  