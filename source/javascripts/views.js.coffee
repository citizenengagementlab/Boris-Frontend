@Views ||= {}

class Views.Carousel extends Backbone.View
  itemSelector: "> .carousel-item"
  width: 600

  events:
    "click .prev": (e) -> @prev()
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
      @carousels[0].to 1

    "change input[name=recent_move]": (e) ->
      return unless e.target.checked
      @carousels[0].to 2

    "change input[name=name_change]": (e) ->
      return unless e.target.checked
      @carousels[1].to 1

  initialize: ->
    @$fieldsets = @$ "fieldset"
    @$inputs = @$ ":text, select, input[type=email], input[type=date]"
    @$button = @$ ".button-primary"

    @carousels = (new Views.Carousel({el}) for el in @$(".carousel"))

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
    @input = @options.input
    @$input = $ @input
    @$input.on "change blur keyup", => @_onChange()
    @$input.on "change blur", => @validate()

    @$input.on "focus", =>
      @showTooltip() unless @valid()

    @$input.on "blur", =>
      @hideTooltip()

    @$input.on "change", =>
      if @valid()
        @hideTooltip()
      else
        @showTooltip()

    @required = @input.required

  value: ->
    $.trim @input.value

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

      @$map.find("#jqvmap1_#{code.toLowerCase()}").click() # XXX Nasty hack because
                                                           # jqvmap doesn't support
                                                           # dynamically setting the
                                                           # selected region.
    @$select.val code.toUpperCase()
    @enableButton()

  enableButton:  -> @$button.prop "disabled", false

  disableButton: -> @$button.prop "disabled", true

