@Views ||= {}


class Views.Form extends Backbone.View
  events:
    "focus input, select": (e) ->
      $el = $ e.target
      $fieldset = $el.closest "fieldset"
      @activateFieldset $fieldset

    "change input[name=has_mailing_address]": (e) ->
      toggleFieldset @$("fieldset.mailing-address"), e.target.checked

    "change input[name=change_of_address]": (e) ->
      toggleFieldset @$("fieldset.previous-address"), e.target.checked

    "change input[name=change_of_name]": (e) ->
      toggleFieldset @$("fieldset.previous-name"), e.target.checked

  openFieldset = ($el) ->
    $el.slideDown()
      .removeClass("closed")
      .find('input, select[name="name_title"], select[name="prev_name_title"]')
      .attr('required', true)

  closeFieldset = ($el) ->
    $el.slideUp().addClass("closed")
      .find('input, select[name="name_title"], select[name="prev_name_title"]')
      .attr('required', false)

  toggleFieldset = ($el, bool) ->
    bool = $el.hasClass("closed") if bool == undefined
    if bool then openFieldset($el) else closeFieldset($el)

  initialize: ->
    @$fieldsets = @$ "fieldset"
    @$inputs = @$ ":text, select, input[type=email], input[type=date], #us_citizen"
    @$button = @$ ".button-primary"

    @fields = for input in @$inputs
      id = input.name
      id = id.charAt(0).toUpperCase() + id.slice(1)
      klassName = id.replace /_\D/g, (match) -> match.charAt(1).toUpperCase()
      klass = Views["#{klassName}FormField"] || Views.FormField
      field = new klass
        el: $(input).closest(".input")
        input: input

      field.on "change", @_onFieldChange, this

      field

    this

  valid: ->
    _.all _.invoke(@fields, "valid"), _.identity

  enableButton: -> @$button.prop "disabled", false

  disableButton: ->
    @$button.prop "disabled", true

  focusInputByIndex: (idx) ->
    @$inputs[idx].focus()

    this

  activateFieldset: ($fieldset) ->
    @$fieldsets.removeClass "active"
    $fieldset.addClass "active" unless $fieldset.hasClass "submit"

    this

  _onFieldChange: ->
    if @valid()
      @enableButton()
    else
      @disableButton()

    this


class Views.FormField extends Backbone.View
  errorMessage: "can't be blank"

  initialize: ->
    @getErrorTip()
    @input = @options.input
    @$input = $ @input
    @$input.on "change blur keyup", => @_onChange()
    @$input.on "change blur", => @validate()

    @$input.on "focus", =>
      @showTooltip() # unless @valid() //always show tooltip onFocus

    @$input.on "blur", =>
      @hideTooltip()
    ###
    @$input.on "change", =>
      if @valid()
        @hideTooltip()
      else
        @showTooltip()
    ###
    @required = ->
      @input.required

  value: ->
    $.trim @input.value

  valid: ->
    value = @value()
    return false if @required() && value == ''

    true

  validate: ->
    if @valid()
      @hideError()
    else
      @showError()

    this

  showTooltip: -> @$el.addClass "tooltip-open"

  hideTooltip: -> @$el.removeClass "tooltip-open"

  showError: -> @$el.addClass "error"

  hideError: -> @$el.removeClass "error"

  getErrorTip: ->
    @$tooltip ||= if @$(".tooltip").length
      @$(".tooltip")
    else
      $("<div class='tooltip'>#{@errorMessage}</div>").appendTo(@el)

  _onChange: ->
    @trigger "change"

class Views.IdNumberFormField extends Views.FormField
  events:
    "click .id-number-hint-icon": "toggleHint"
  valid: ->
    if @value()
      re = /^(none|\d{4}|[-*A-Z0-9]{7,42})$/i
      if !@value.match(re)
        return false
    return true

  toggleHint: ->
    @$el.toggleClass "tooltip-open"

class Views.RaceFormField extends Views.FormField
  valid: ->
    if @required()
      return @value() != "Select One..."
    true

class Views.PartyFormField extends Views.FormField
  valid: ->
    if @required()
      return @value() != "Select One..."
    true

class Views.NameTitleFormField extends Views.FormField
  valid: ->
    if @required()
      return @value() != "--"
    true

class Views.PrevNameTitleFormField extends Views.FormField
  valid: ->
    if @required()
      return @value() != "--"
    true

class Views.HomeZipCodeFormField extends Views.FormField
  errorMessage: "Enter a valid 5 digit zip code."
  valid: =>
    if @required()
      return super && @value().length == 5
    else
      true

class Views.MailingZipCodeFormField extends Views.HomeZipCodeFormField
  valid: =>
    super()

class Views.PrevZipCodeFormField extends Views.HomeZipCodeFormField
  valid: =>
    super()

class Views.EmailAddressFormField extends Views.FormField
  errorMessage: "Enter a valid email address"
  valid: =>
    re = /^(([^<>()\[\]\\.,;:\s@\"]+(\.[^<>()\[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    super && re.test(@value())

class Views.DateOfBirthFormField extends Views.HomeZipCodeFormField
  errorMessage: 'Enter your birthdate in MM/DD/YYYY format'
  valid: =>
    if !@value().match(/^(0[1-9]|1[012])[- \/.](0[1-9]|[12][0-9]|3[01])[- \/.](19|20)\d\d+$/)
      return false
    # Check Age
    today    = new Date()
    birthday = new Date(@value())
    age      = today.getFullYear() - birthday.getFullYear()
    month    = today.getMonth() - birthday.getMonth
    if (month < 0 || (month == 0 && today.getDate() < birthday.getDate()))
      age--

    if age < 17
      @$input.siblings('.tooltip').text "You must turn 18 by the next election to register to vote."
      return false
    true

class Views.PhoneFormField extends Views.FormField
  errorMessage: "Enter a phone number in xxx-xxx-xxxx format"
  valid: =>
    if @$input.attr('required') == true || @value().length > 0
      re = /(1-)?[(]*(\d{3})[) -.]*(\d{3})[ -.]*(\d{4})\D*/
      return re.test(@value())
    return true

class Views.UsCitizenFormField extends Views.FormField
  errorMessage: "Must be a citizen to register"
  initialize: ->
    super()
    @$input.on "change", =>
      if @valid()
        @hideTooltip()
      else
        @showTooltip()
  valid: =>
    if !@$input.attr('checked')
      return false
    true

class Views.State extends Backbone.View
  events:
    "change select":           "selectState"
    "regionClick.jqvmap #map": "selectState"

  initialize: ->
    @$button = @$ ".button-primary"
    @$select = @$ "#state"
    @$map    = @$ "#map"

    @$map.vectorMap
      backgroundColor: "transparent"
      borderColor:     "#A1A09F"
      borderOpacity:   1
      borderWidth:     1
      color:           "transparent"
      enableZoom:      false
      map:             "usa_en"
      selectedColor:   "#21CB00"
      showTooltip:     true

    @$path = $("<path/>").css(display: "none").appendTo(@$map.find("svg g"))

  selectState: (event, code) ->
    unless code
      code = @$select.val()
      unless code
        @disableButton()
        try @$path.click()
        return

      @$map.find("#jqvmap1_#{code.toLowerCase('')}").click() # XXX Nasty hack because
                                                           # jqvmap doesn't support
                                                           # dynamically setting the
                                                           # selected region.
    @$select.val code.toUpperCase()
    @$select.trigger 'focus'
    @enableButton()


  enableButton:  -> @$button.prop "disabled", false

  disableButton: -> @$button.prop "disabled", true
