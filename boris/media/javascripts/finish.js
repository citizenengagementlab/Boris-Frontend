(function() {
  var Ellipsis, checkPdfUrl,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  Ellipsis = (function(_super) {

    __extends(Ellipsis, _super);

    function Ellipsis() {
      this.stop = __bind(this.stop, this);

      this.play = __bind(this.play, this);
      return Ellipsis.__super__.constructor.apply(this, arguments);
    }

    Ellipsis.prototype.tagName = "span";

    Ellipsis.prototype.className = "Ellipsis";

    Ellipsis.prototype.states = ['', '.', '..', '...'];

    Ellipsis.prototype.initialize = function($el) {
      this.$el = $el;
      this.run = true;
      this.count = 0;
      return this.play();
    };

    Ellipsis.prototype.render = function() {
      return this.$el.text(this.states[this.count % 4]);
    };

    Ellipsis.prototype.play = function() {
      this.count += 1;
      this.render();
      if (this.run) {
        return setTimeout(this.play, 500);
      }
    };

    Ellipsis.prototype.stop = function() {
      return this.run = false;
    };

    return Ellipsis;

  })(Backbone.View);

  checkPdfUrl = function() {
    var a, downloadLink, proxyUrl;
    downloadLink = $('a.download').attr('href');
    a = $('<a />');
    a.attr('href',downloadLink);
    proxyUrl = '/rtv'+a[0].pathname;
    return $.ajax({
      url: proxyUrl,
      type: "HEAD",
      cache: false,
      error: function(xhr, status, err) {
        if (status !== "Unknown") {
          setTimeout(checkPdfUrl, 1000);
        }
        if (status === "Unknown") {
          return setTimeout(function() {
            $('#waiting').hide();
            return $('#download').show();
          }, 2000);
        }
      },
      success: function(d) {
        window.ellipsis.stop();
        return $('#waiting').fadeOut(function() {
          return $('#download').fadeIn();
        });
      }
    });
  };

  $(function() {
    $('#download').hide();
    window.ellipsis = new Ellipsis($('span.ellipsis'));
    return setTimeout(checkPdfUrl, 3000);
  });

}).call(this);