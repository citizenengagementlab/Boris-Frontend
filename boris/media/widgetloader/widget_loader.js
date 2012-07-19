// Generated by CoffeeScript 1.3.3

$(function() {
  var registrationLinks;
  $('a.ovr-close').live('click', function(e) {
    var close;
    e.preventDefault();
    close = confirm("Are you sure you want to close the voter registration form?");
    if (close) {
      return $('.ovr-overlay, #ovr-container').remove();
    } else {
      return false;
    }
  });
  registrationLinks = $('a.floatbox[href*="rockthevote.com/registrants/new"]');
  return registrationLinks.on('click', function(e) {
    var $body, $close, $container, $el, $iframe, $overlay;
    e.preventDefault();
    $el = $(this);
    $body = $('body');
    $overlay = $('<div class="ovr-overlay" />');
    $iframe = $('<iframe id="ovr-widget" />');
    $close = $('<a href="#" class="ovr-close">close [x]</a>');
    $container = $('<div id="ovr-container" />');
    $iframe.attr('src', $el.attr('href'));
    $body.append($container);
    $container.append($overlay);
    $overlay.hide().fadeIn(300);
    $container.append($iframe);
    return $container.prepend($close);
  });
});
