@Views ||= {}


class Views.Form extends Backbone.View
  events:
    "focus input, select": (e) ->
      $el = $ e.target
      $fieldset = $el.closest "fieldset"
      @activateFieldset $fieldset

  initialize: ->
    @$fieldsets = @$ "fieldset"
    @$inputs = @$ ":text, select, input[type=email], input[type=date]"
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

  enableButton: ->
    @$button.prop "disabled", false

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
  required: true
  errorMessage: "can't be blank"

  initialize: ->
    @input = @options.input
    @$input = $ @input
    @$input.on "change blur keyup", => @_onChange()
    @$input.on "change blur", => @validate()

    @$input.on "focus", =>
      @showTooltip() unless @valid()

    @$input.on "blur", =>
      @hideTooltip()

  value: ->
    $.trim @input.value + ''

  valid: ->
    value = @value()
    return false if @required && value == ''

    true

  validate: ->
    @getErrorTip()

    if @valid()
      @hideError()
    else
      @showError()

    this

  showTooltip: ->
    @$el.addClass "tooltip-open"
    this

  hideTooltip: ->
    @$el.removeClass "tooltip-open"
    this

  showError: ->
    @$el.addClass "error"
    this

  hideError: ->
    @$el.removeClass "error"
    this

  getErrorTip: ->
    @$tooltip ||= if @$(".tooltip").length
      @$(".tooltip")
    else
      $("<div class='tooltip'>#{@errorMessage}</div>").appendTo(@el)

  _onChange: ->
    @trigger "change"


class Views.ZipCodeFormField extends Views.FormField

class Views.SuffixFormField extends Views.FormField
  required: false

class Views.IdNumberFormField extends Views.FormField
  events:
    "click .id-number-hint-icon": "toggleHint"

  toggleHint: ->
    @$el.toggleClass "tooltip-open"

class Views.RaceOrEthnicGroupFormField extends Views.FormField
  valid: ->
    super && @value() != "Select One..."

class Views.PoliticalPartyFormField extends Views.FormField
  valid: ->
    super && @value() != "Select One..."

