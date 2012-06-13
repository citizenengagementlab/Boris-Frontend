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

    @fields = for input in @$inputs
      id = input.name
      id = id.charAt(0).toUpperCase() + id.slice(1)
      klassName = id.replace /_\D/g, (match) -> match.charAt(1).toUpperCase()
      klass = Views["#{klassName}FormField"] || Views.FormField
      new klass el: $(input).closest(".input")

    this

  focusInputByIndex: (idx) ->
    @$inputs[idx].focus()

    this

  activateFieldset: ($fieldset) ->
    @$fieldsets.removeClass "active"
    $fieldset.addClass "active" unless $fieldset.hasClass "submit"

    this


class Views.FormField extends Backbone.View


class Views.ZipCodeFormField extends Views.FormField


class Views.IdNumberFormField extends Views.FormField
  events:
    "click .id-number-hint-icon": "toggleHint"

  toggleHint: ->
    @$el.toggleClass "hint-open"

