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

    $el.on("change blur focus keyup", function() {
      $fake.toggleClass("checked", $el.prop("checked"));
    })

    // $fake.on("click", function(){
    //   $el.prop("checked", !$el.prop("checked")).trigger("change")
    // });
  });
})
