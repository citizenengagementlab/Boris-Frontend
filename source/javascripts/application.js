//= require underscore
//= require backbone
//= require views
//= require form

$(function(){
  $(":checkbox").each(function(){
    var $el = $(this)
    var $fake = $("<div class='fake-checkbox'></div>")

    $el.wrap("<div class='fake-checkbox-wrap'></div>")
    $el.parent().append($fake)

    var check = function() {
      $fake.toggleClass("checked", $el.prop("checked"));
      $fake.toggleClass("focus", document.activeElement == this);
    }

    $el.on("change blur focus keyup", check);

  });
})
