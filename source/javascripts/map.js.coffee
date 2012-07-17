#= require jquery.vmap
#= require jquery.vmap.usa

if Modernizr.inlinesvg and Modernizr.svg
  @form = form = new Views.State
    el: $ ".state-form"
  form.disableButton()