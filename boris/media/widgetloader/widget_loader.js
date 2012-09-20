var head, isVersion, injectjQuery, initializeWidget, script;

/**
 * Used for version test cases.
 *
 * @param {string} left A string containing the version that will become
 *        the left hand operand.
 * @param {string} oper The comparison operator to test against. By
 *        default, the "==" operator will be used.
 * @param {string} right A string containing the version that will
 *        become the right hand operand. By default, the current jQuery
 *        version will be used.
 *
 * @return {boolean} Returns the evaluation of the expression, either
 *         true or false.
 */
isVersion = function(left, oper, right) {
    if (left) {
        var pre = /pre/i,
            replace = /[^\d]+/g,
            oper = oper || "==",
            right = right || $().jquery,
            l = left.replace(replace, ''),
            r = right.replace(replace, ''),
            l_len = l.length, r_len = r.length,
            l_pre = pre.test(left), r_pre = pre.test(right);

        l = (r_len > l_len ? parseInt(l) * ((r_len - l_len) * 10) : parseInt(l));
        r = (l_len > r_len ? parseInt(r) * ((l_len - r_len) * 10) : parseInt(r));

        switch(oper) {
            case "==": {
                return (true === (l == r && (l_pre == r_pre)));
            }
            case ">=": {
                return (true === (l >= r && (!l_pre || l_pre == r_pre)));
            }
            case "<=": {
                return (true === (l <= r && (!r_pre || r_pre == l_pre)));
            }
            case ">": {
                return (true === (l > r || (l == r && r_pre)));
            }
            case "<": {
                return (true === (l < r || (l == r && l_pre)));
            }
        }
    }

    return false;
}

initializeWidget = function($) {
  var head, ovrCss, registrationLinks;
  ovrCss = document.createElement("link");
  ovrCss.href = 'https://register2.rockthevote.com/widget_loader.css';
  ovrCss.rel = "stylesheet";
  ovrCss.type = "text/css";
  head = document.getElementsByTagName("head")[0];
  head.appendChild(ovrCss);
  registrationLinks = $('.floatbox[href*="register.rockthevote.com"],.floatbox[href*="register2.rockthevote.com"]');
  return registrationLinks.on('click', function(e) {
    var $body, $close, $container, $el, $iframe, $overlay;
    e.preventDefault();
    $el = $(this);
    $body = $('body');
    $overlay = $('<div class="ovr-overlay" />');
    $iframe = $('<iframe id="ovr-widget" />');
    $close = $('<a href="#" class="ovr-close">[x]</a>');
    $container = $('<div id="ovr-container" />');
    $iframe.attr('src', $el.attr('href'));
    $body.append($container);
    $container.append($overlay);
    $overlay.hide().fadeIn(300);
    $container.append($iframe);
    $container.prepend($close);
    return $close.on('click', function(e) {
      var close;
      e.preventDefault();
      close = confirm("Close voter registration form?");
      if (close) {
        return $('.ovr-overlay, #ovr-container').remove();
      } else {
        return false;
      }
    });
  });
};

injectjQuery = function() {
  script = document.createElement("script");
  script.src = "http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js";
  head = document.getElementsByTagName("head")[0];
  head.appendChild(script);
  script.onload = function() {
    return initializeWidget(jQuery);
  }
}

if (typeof jQuery === "undefined") {
  injectjQuery();
} else if (isVersion(jQuery.fn.jquery,"<","1.7")) {
  injectjQuery();
} else {
  initializeWidget(jQuery);
}
