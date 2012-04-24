tabs = ->
  $("document").ready ->
    $("fieldset:not(:first)").hide()
    $("nav").show()
    $("nav li a:first").addClass "tab-active"
    $("legend").hide()
    buttons = "<input type=\"button\" class=\"next-button\" value=\"Continue\" /><input type=\"button\" data-tab=\"\" class=\"prev-button\" value=\"Go Back\" />"
    $("fieldset:not(:first)").each ->
      $fs = $(this)
      $fs.append buttons
      id = $fs.attr("id")
      switch id
        when "address"
          $fs.children(".next-button").on "click", (e) ->
            false  unless validateAddresses()
        when "personal"
          $fs.children(".next-button").on "click", (e) ->
            false  unless validatePersonal()
        when "contact"
          $fs.children(".next-button").on "click", (e) ->
            false  unless validateContact()
        when "additional"
          $fs.children(".next-button").on "click", (e) ->
            false  unless validateAdditional()
        else
          false

    $("fieldset#additional").find("input.next-button").hide()
    $("input#get_started").click ->
      unless validateStartFields()
        $("fieldset#get_started").hide()
        $("fieldset#address").show()
        $("nav li a").removeClass "tab-active"
        $("nav li a#address").addClass "tab-active"

    $("fieldset#address .prev-button").click ->
      $("fieldset#address").hide()
      $("fieldset#get_started").show()
      $("nav li a").removeClass "tab-active"
      $("nav li a#address").addClass "tab-active"

    $(".next-button").click ->
      $(this).parent("fieldset").hide()
      $fieldsetNext = $(this).parent("fieldset").next("fieldset")
      $fieldsetNext.show()
      $("nav li a").removeClass "tab-active"
      $("nav li a").filter("#" + $fieldsetNext.attr("id")).addClass "tab-active"

    $(".prev-button").click ->
      $(this).parent("fieldset").hide()
      $fieldsetPrev = $(this).parent("fieldset").prev("fieldset")
      $fieldsetPrev.show()
      $("nav li a").removeClass "tab-active"
      $("nav li a").filter("#" + $fieldsetPrev.attr("id")).addClass "tab-active"