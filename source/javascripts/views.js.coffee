@Views ||= {}

class Views.Carousel extends Backbone.View
  itemSelector: "> .carousel-item"
  width: 600

  events:
    "click .next": (e) -> @next()
    "click .back": (e) -> @to 0

  initialize: ->
    @$items = @$(@itemSelector)
    @currentIndex = 0

    $(item).css(left: i * @width) for i, item of @$items

  itemForIndex: (idx) ->
    @$items.eq idx

  to: (idx) ->
    $(item).css(left: (i - idx) * @width) for i, item of @$items
    @currentIndex = idx

  next: -> @to @currentIndex + 1

  prev: -> @to @currentIndex - 1

class Views.Form extends Backbone.View
  events:
    "focus input, select": (e) ->
      $el = $ e.target
      $fieldset = $el.closest "fieldset"
      @activateFieldset $fieldset

    "change input[name=mailing_address]": (e) ->
      return unless e.target.checked
      @$(".multi .stage").css(left: "-=600px")

    "change input[name=recent_move]": (e) ->
      return unless e.target.checked
      @$(".multi .stage").css(left: "-=1200px")

  initialize: ->
    @$fieldsets = @$ "fieldset"
    @$inputs = @$ ":text, select, input[type=email], input[type=date]"
    @$button = @$ ".button-primary"

    new Views.Carousel({el}) for el in @$(".carousel")

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

