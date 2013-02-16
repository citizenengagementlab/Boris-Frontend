(function() {
  $('#setlang select').change(function() {
    this.form.submit();
  });
  $('#setlang input[type="submit"]').hide();
}).call(this);