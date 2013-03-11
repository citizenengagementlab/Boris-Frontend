(function() {
  var $bottomShadow, $main, $topShadow, check, content, form, requestAnimFrame;

  this.form = form = new Views.Form({
    el: $(".registration-form")
  });

  //form.focusInputByIndex(0);

  form.disableButton();

  requestAnimFrame = (function() {
    return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame || function(callback) {
      return window.setTimeout(callback, 1000 / 60);
    };
  })();

  content = document.getElementById("content");

  $main = $("#main");

  $topShadow = $(".scroll-shadows.top");

  $bottomShadow = $(".scroll-shadows.bottom");

  check = function() {
    if (content.scrollHeight !== content.offsetHeight) {
      $main.addClass('scrollable');
    } else {
      $main.removeClass('scrollable');
    }
    if (content.scrollTop === 0) {
      $topShadow.addClass('at-top');
    } else if (content.scrollHeight === content.offsetHeight + content.scrollTop) {
      $bottomShadow.addClass('at-bottom');
    } else {
      $topShadow.removeClass('at-top');
      $bottomShadow.removeClass('at-bottom');
    }
    return requestAnimFrame(check);
  };

  decodeURLParams = function() {
    //pull url parameters into fields
    var url_params = window.location.search.split('&');
    for (var i in url_params) {
      var p = url_params[i];
      var field = p.split('=')[0].replace('?','');
      var value = p.split('=')[1];

      if (field == "source") { return; } //don't pull source, we do that in middleware
      if (field == "name_title") {
        $('select[name="name_title"] option[value="'+decodeURIComponent(value)+'"]').attr('selected','selected');
        $('select[name="name_title"]').siblings('.fake-select').html(value);
      } else {
        $('input[name="'+field+'"]').val(decodeURIComponent(value)).trigger('change');
      }
    }
  };

  check();
  decodeURLParams();

}).call(this);
