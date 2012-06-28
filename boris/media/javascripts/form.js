(function() {
  var form;

  this.form = form = new Views.Form({
    el: $(".registration-form")
  });

  form.focusInputByIndex(0);

  form.disableButton();

}).call(this);
