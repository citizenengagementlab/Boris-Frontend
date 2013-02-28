(function() {

  $(function() {
    $(":checkbox").each(function() {
      var $el, $fake, check;
      $el = $(this);
      $fake = $("<div class='fake-checkbox'></div>");
      $fake.addClass($el.attr("class"));
      $el.wrap("<div class='fake-checkbox-wrap'></div>");
      $el.parent().append($fake);
      check = function() {
        $fake.toggleClass("checked", $el.prop("checked"));
        return $fake.toggleClass("focus", document.activeElement === this);
      };
      $el.on("change blur focus keyup", check);
      check();
      return this;
    });
    return $("select").each(function() {
      var $el, $fake, check;
      $el = $(this);
      $fake = $("<div class='fake-select'></div>");
      $fake.addClass($el.attr("class"));
      $el.wrap("<div class='fake-select-wrap'></div>");
      $el.parent().append($fake);
      check = function() {
        $fake.text($el.children('option:selected').text());
        return $fake.toggleClass("focus", document.activeElement === this);
      };
      $el.on("change blur focus keyup", check);
      check();
      return this;
    });
  });

}).call(this);
