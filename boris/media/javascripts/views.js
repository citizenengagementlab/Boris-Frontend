(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  this.Views || (this.Views = {});

  Views.Form = (function(_super) {
    var closeFieldset, openFieldset, toggleFieldset;

    __extends(Form, _super);

    function Form() {
      this._onSubmit = __bind(this._onSubmit, this);
      return Form.__super__.constructor.apply(this, arguments);
    }

    Form.prototype.events = {
      "focus input, select": function(e) {
        var $el, $fieldset;
        $el = $(e.target);
        $fieldset = $el.closest("fieldset");
        return this.activateFieldset($fieldset);
      },
      "change input[name=has_mailing_address]": function(e) {
        return toggleFieldset(this.$("fieldset.mailing-address"), e.target.checked);
      },
      "change input[name=change_of_address]": function(e) {
        return toggleFieldset(this.$("fieldset.previous-address"), e.target.checked);
      },
      "change input[name=change_of_name]": function(e) {
        return toggleFieldset(this.$("fieldset.previous-name"), e.target.checked);
      }
    };

    openFieldset = function($el) {
      return $el.slideDown().removeClass("closed").find('input, select[name="name_title"], select[name="prev_name_title"]').attr('required', true);
    };

    closeFieldset = function($el) {
      return $el.slideUp().addClass("closed").find('input, select[name="name_title"], select[name="prev_name_title"]').attr('required', false);
    };

    toggleFieldset = function($el, bool) {
      if (bool === void 0) {
        bool = $el.hasClass("closed");
      }
      if (bool) {
        return openFieldset($el);
      } else {
        return closeFieldset($el);
      }
    };

    Form.prototype.initialize = function() {
      var field, id, input, klass, klassName;
      this.$fieldsets = this.$("fieldset");
      this.$inputs = this.$(":text, select, input[type=email], input[type=date], #us_citizen");
      this.$button = this.$(".button-primary");
      this.$button.on('click', this._onSubmit);
      this.fields = (function() {
        var _i, _len, _ref, _results;
        _ref = this.$inputs;
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          input = _ref[_i];
          id = input.name;
          id = id.charAt(0).toUpperCase() + id.slice(1);
          klassName = id.replace(/_\D/g, function(match) {
            return match.charAt(1).toUpperCase();
          });
          klass = Views["" + klassName + "FormField"] || Views.FormField;
          field = new klass({
            el: $(input).closest(".input"),
            input: input
          });
          field.on("change", this._onFieldChange, this);
          _results.push(field);
        }
        return _results;
      }).call(this);
      return this;
    };

    Form.prototype.valid = function() {
      return _.all(_.invoke(this.fields, "valid"), _.identity);
    };

    Form.prototype.enableButton = function() {
      return this.$button.removeClass("disabled");
    };

    Form.prototype.disableButton = function() {
      return this.$button.addClass("disabled");
    };

    Form.prototype.focusInputByIndex = function(idx) {
      this.$inputs[idx].focus();
      return this;
    };

    Form.prototype.activateFieldset = function($fieldset) {
      this.$fieldsets.removeClass("active");
      if (!$fieldset.hasClass("submit")) {
        $fieldset.addClass("active");
      }
      return this;
    };

    Form.prototype._onFieldChange = function() {
      if (this.valid()) {
        this.enableButton();
      } else {
        this.disableButton();
      }
      return this;
    };

    Form.prototype._onSubmit = function(e) {
      var $errorList, errors, html;
      if (this.$button.hasClass('disabled')) {
        e.preventDefault();
        errors = [];
        this.fields.forEach(function(field) {
          field.validate();
          if (!field.valid()) {
            return errors.push({
              name: field.$input.siblings('label').text(),
              error: field.errorMessage
            });
          }
        });
        $('.error-list').remove();
        $errorList = $("<ul class='error-list'></ul>");
        html = "<h2>Please correct the following errors:</h2>";
        errors.forEach(function(error) {
          if (error.name) {
            return html += "<li>" + error.name + ": " + error.error + "</li>";
          } else {
            return html += "<li>" + error.error + "</li>";
          }
        });
        $errorList.html(html);
        $('fieldset.submit').prepend($errorList);
        return false;
      } else {
        return true;
      }
    };

    return Form;

  })(Backbone.View);

  Views.FormField = (function(_super) {

    __extends(FormField, _super);

    function FormField() {
      return FormField.__super__.constructor.apply(this, arguments);
    }

    FormField.prototype.errorMessage = "Required";

    FormField.prototype.initialize = function() {
      var _this = this;
      this.getErrorTip();
      this.input = this.options.input;
      this.$input = $(this.input);
      this.$input.on("change blur keyup", function() {
        return _this._onChange();
      });
      this.$input.on("change blur", function() {
        return _this.validate();
      });
      this.$input.on("focus", function() {
        return _this.showTooltip();
      });
      this.$input.on("blur", function() {
        return _this.hideTooltip();
      });
      /*
          @$input.on "change", =>
            if @valid()
              @hideTooltip()
            else
              @showTooltip()
      */

      return this.required = function() {
        return this.input.required;
      };
    };

    FormField.prototype.value = function() {
      return $.trim(this.input.value);
    };

    FormField.prototype.valid = function() {
      var value;
      value = this.value();
      if (this.required() && value === '') {
        return false;
      }
      return true;
    };

    FormField.prototype.validate = function() {
      if (this.valid()) {
        this.hideError();
      } else {
        this.showError();
      }
      return this;
    };

    FormField.prototype.showTooltip = function() {
      return this.$el.addClass("tooltip-open");
    };

    FormField.prototype.hideTooltip = function() {
      return this.$el.removeClass("tooltip-open");
    };

    FormField.prototype.showError = function() {
      return this.$el.addClass("error");
    };

    FormField.prototype.hideError = function() {
      return this.$el.removeClass("error");
    };

    FormField.prototype.getErrorTip = function() {
      return this.$tooltip || (this.$tooltip = this.$(".tooltip").length ? this.$(".tooltip") : $("<div class='tooltip'>" + this.errorMessage + "</div>").appendTo(this.el));
    };

    FormField.prototype._onChange = function() {
      return this.trigger("change");
    };

    return FormField;

  })(Backbone.View);

  Views.IdNumberFormField = (function(_super) {

    __extends(IdNumberFormField, _super);

    function IdNumberFormField() {
      return IdNumberFormField.__super__.constructor.apply(this, arguments);
    }

    IdNumberFormField.prototype.events = {
      "click .id-number-hint-icon": "toggleHint"
    };

    IdNumberFormField.prototype.valid = function() {
      if (this.value()) {
        return /^(none|\d{4}|[-*A-Z0-9]{7,42})$/i.test(this.value());
      }
      return true;
    };

    IdNumberFormField.prototype.toggleHint = function() {
      return this.$el.toggleClass("tooltip-open");
    };

    return IdNumberFormField;

  })(Views.FormField);

  Views.RaceFormField = (function(_super) {

    __extends(RaceFormField, _super);

    function RaceFormField() {
      return RaceFormField.__super__.constructor.apply(this, arguments);
    }

    RaceFormField.prototype.errorMessage = "Enter your race or ethnic group.";

    RaceFormField.prototype.valid = function() {
      if (this.required()) {
        return this.value() !== "Select One...";
      }
      return true;
    };

    return RaceFormField;

  })(Views.FormField);

  Views.PartyFormField = (function(_super) {

    __extends(PartyFormField, _super);

    function PartyFormField() {
      return PartyFormField.__super__.constructor.apply(this, arguments);
    }

    PartyFormField.prototype.errorMessage = "Select your political affiliation.";

    PartyFormField.prototype.valid = function() {
      if (this.required()) {
        return this.value() !== "Select One...";
      }
      return true;
    };

    return PartyFormField;

  })(Views.FormField);

  Views.NameTitleFormField = (function(_super) {

    __extends(NameTitleFormField, _super);

    function NameTitleFormField() {
      return NameTitleFormField.__super__.constructor.apply(this, arguments);
    }

    NameTitleFormField.prototype.errorMessage = "Title is required.";

    NameTitleFormField.prototype.valid = function() {
      if (this.required()) {
        return this.value() !== "--";
      }
      return true;
    };

    return NameTitleFormField;

  })(Views.FormField);

  Views.PrevNameTitleFormField = (function(_super) {

    __extends(PrevNameTitleFormField, _super);

    function PrevNameTitleFormField() {
      return PrevNameTitleFormField.__super__.constructor.apply(this, arguments);
    }

    PrevNameTitleFormField.prototype.valid = function() {
      if (this.required()) {
        return this.value() !== "--";
      }
      return true;
    };

    return PrevNameTitleFormField;

  })(Views.FormField);

  Views.HomeZipCodeFormField = (function(_super) {

    __extends(HomeZipCodeFormField, _super);

    function HomeZipCodeFormField() {
      this.valid = __bind(this.valid, this);
      return HomeZipCodeFormField.__super__.constructor.apply(this, arguments);
    }

    HomeZipCodeFormField.prototype.errorMessage = "Enter a valid 5 digit zip code.";

    HomeZipCodeFormField.prototype.valid = function() {
      if (this.required()) {
        return /^((\d{5}(-\d{4}))|(\d{5}))$/.test(this.value());
      } else {
        return true;
      }
    };

    return HomeZipCodeFormField;

  })(Views.FormField);

  Views.MailingZipCodeFormField = (function(_super) {

    __extends(MailingZipCodeFormField, _super);

    function MailingZipCodeFormField() {
      this.valid = __bind(this.valid, this);
      return MailingZipCodeFormField.__super__.constructor.apply(this, arguments);
    }

    MailingZipCodeFormField.prototype.valid = function() {
      return MailingZipCodeFormField.__super__.valid.call(this);
    };

    return MailingZipCodeFormField;

  })(Views.HomeZipCodeFormField);

  Views.PrevZipCodeFormField = (function(_super) {

    __extends(PrevZipCodeFormField, _super);

    function PrevZipCodeFormField() {
      this.valid = __bind(this.valid, this);
      return PrevZipCodeFormField.__super__.constructor.apply(this, arguments);
    }

    PrevZipCodeFormField.prototype.valid = function() {
      return PrevZipCodeFormField.__super__.valid.call(this);
    };

    return PrevZipCodeFormField;

  })(Views.HomeZipCodeFormField);

  Views.EmailAddressFormField = (function(_super) {

    __extends(EmailAddressFormField, _super);

    function EmailAddressFormField() {
      this.valid = __bind(this.valid, this);
      return EmailAddressFormField.__super__.constructor.apply(this, arguments);
    }

    EmailAddressFormField.prototype.errorMessage = "Enter a valid email address";

    EmailAddressFormField.prototype.valid = function() {
      var re;
      re = /^(([^<>()\[\]\\.,;:\s@\"]+(\.[^<>()\[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return EmailAddressFormField.__super__.valid.apply(this, arguments) && re.test(this.value());
    };

    return EmailAddressFormField;

  })(Views.FormField);

  Views.DateOfBirthFormField = (function(_super) {

    __extends(DateOfBirthFormField, _super);

    function DateOfBirthFormField() {
      this.valid = __bind(this.valid, this);
      return DateOfBirthFormField.__super__.constructor.apply(this, arguments);
    }

    DateOfBirthFormField.prototype.errorMessage = 'Enter your birthdate in MM/DD/YYYY format';

    DateOfBirthFormField.prototype.valid = function() {
      var age, birthday, month, today;
      if (!this.value().match(/^(0[1-9]|1[012])[- \/.](0[1-9]|[12][0-9]|3[01])[- \/.](19|20)\d\d+$/)) {
        return false;
      }
      today = new Date();
      birthday = new Date(this.value());
      age = today.getFullYear() - birthday.getFullYear();
      month = today.getMonth() - birthday.getMonth;
      if (month < 0 || (month === 0 && today.getDate() < birthday.getDate())) {
        age--;
      }
      if (age < 17) {
        this.$input.siblings('.tooltip').text("You must turn 18 by the next election to register to vote.");
        return false;
      }
      return true;
    };

    return DateOfBirthFormField;

  })(Views.HomeZipCodeFormField);

  Views.PhoneFormField = (function(_super) {

    __extends(PhoneFormField, _super);

    function PhoneFormField() {
      this.valid = __bind(this.valid, this);
      return PhoneFormField.__super__.constructor.apply(this, arguments);
    }

    PhoneFormField.prototype.errorMessage = "Enter a phone number in xxx-xxx-xxxx format";

    PhoneFormField.prototype.valid = function() {
      var re;
      if (this.$input.attr('required') === true || this.value().length > 0) {
        re = /(1-)?[(]*(\d{3})[) -.]*(\d{3})[ -.]*(\d{4})\D*/;
        return re.test(this.value());
      }
      return true;
    };

    return PhoneFormField;

  })(Views.FormField);

  Views.UsCitizenFormField = (function(_super) {

    __extends(UsCitizenFormField, _super);

    function UsCitizenFormField() {
      this.valid = __bind(this.valid, this);
      return UsCitizenFormField.__super__.constructor.apply(this, arguments);
    }

    UsCitizenFormField.prototype.errorMessage = "Must be a citizen to register";

    UsCitizenFormField.prototype.initialize = function() {
      var _this = this;
      UsCitizenFormField.__super__.initialize.call(this);
      return this.$input.on("change", function() {
        if (_this.valid()) {
          return _this.hideTooltip();
        } else {
          return _this.showTooltip();
        }
      });
    };

    UsCitizenFormField.prototype.valid = function() {
      if (!this.$input.attr('checked')) {
        return false;
      }
      return true;
    };

    return UsCitizenFormField;

  })(Views.FormField);

  Views.State = (function(_super) {

    __extends(State, _super);

    function State() {
      return State.__super__.constructor.apply(this, arguments);
    }

    State.prototype.events = {
      "change select": "selectState",
      "regionClick.jqvmap #map": "selectState"
    };

    State.prototype.initialize = function() {
      this.$button = this.$(".button-primary");
      this.$select = this.$("#state");
      this.$map = this.$("#map");
      this.$map.vectorMap({
        backgroundColor: "transparent",
        borderColor: "#A1A09F",
        borderOpacity: 1,
        borderWidth: 1,
        color: "transparent",
        enableZoom: false,
        map: "usa_en",
        selectedColor: "#21CB00",
        showTooltip: true
      });
      return this.$path = $("<path/>").css({
        display: "none"
      }).appendTo(this.$map.find("svg g"));
    };

    State.prototype.selectState = function(event, code) {
      if (!code) {
        code = this.$select.val();
        if (!code) {
          this.disableButton();
          try {
            this.$path.click();
          } catch (_error) {}
          return;
        }
        this.$map.find("#jqvmap1_" + (code.toLowerCase(''))).click();
      }
      this.$select.val(code.toUpperCase());
      this.$select.trigger('focus');
      return this.enableButton();
    };

    State.prototype.enableButton = function() {
      return this.$button.prop("disabled", false);
    };

    State.prototype.disableButton = function() {
      return this.$button.prop("disabled", true);
    };

    return State;

  })(Backbone.View);

}).call(this);
