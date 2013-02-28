$ ->
  $(":checkbox").each ->
    $el = $ this
    $fake = $ "<div class='fake-checkbox'></div>"
    $fake.addClass $el.attr "class"

    $el.wrap "<div class='fake-checkbox-wrap'></div>"
    $el.parent().append($fake)

    check = ->
      $fake.toggleClass("checked", $el.prop("checked"))
      $fake.toggleClass("focus", document.activeElement == this)

    $el.on("change blur focus keyup", check)
    check()
    this


  $("select").each ->
    $el = $ this
    $fake = $ "<div class='fake-select'></div>"
    $fake.addClass $el.attr "class"

    $el.wrap "<div class='fake-select-wrap'></div>"
    $el.parent().append($fake)

    check = ->
      $fake.text $el.val()
      $fake.toggleClass("focus", document.activeElement == this)

    $el.on("change blur focus keyup", check)
    check()
    this
