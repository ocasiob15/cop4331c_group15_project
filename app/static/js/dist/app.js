(function () {

  window.app = window.app || {};

  app.api_endpoint = function (options) {

    options = options         || {};
    options.url = options.url || "";

    options.url = app.site_root() + options.url;

    // override anything else necessary

    // return promisified request
    return $.ajax(options);

  };

})();

(function () {

  var controllers = {};

  // top level application code 
  app.controller = function (name, callback) {

    // define a callback for the controller name
    controllers[name] = callback;

  };

  function bind_controllers () {

    // get all elements with this attribute
    $controlled = $('[data-controller]');

    // go through each one and get the name of that controller
    $controlled.each(function (index, elem) {

      $elem = $(elem);

      var controller = $elem.attr('data-controller');

      // pass element into controller
      controllers[controller]($elem);

    });

  }

  app.bind_controllers = bind_controllers;

})();

(function () {

  var api_endpoint = app.api_endpoint;
  
  // do the thing
  $.fn.ajaxify = function (configs) {

    configs = configs || {};

    var on_validate, on_send, on_result, on_error;

    on_validate = configs.on_validate || function () { return true };
    on_send     = configs.on_send     || function () {};
    on_result   = configs.on_result   || function () {};
    on_error    = configs.on_error    || function () {};

    var $this = $(this);

    if (!$this.is('form')) {

      console.error("ajaxify must be called on a form");

      return

    }

    $this.addClass('ajaxified');

    $this.submit(function (e) {

      e.preventDefault();
      
      var method, action, inputs;

      method = $this.attr('method');
      action = $this.attr('action');

      inputs = $('input,textarea,select', $this)
      inputs = inputs.not('input[type=submit],input[type=radio]:not(:checked),input[type=checkbox]:not(:checked)');

      var data = {};

      for (var i = 0; i < inputs.length; i++) {

        var $input, value, name;

        $input = $(inputs[i]);

        value = $input.val();

        name  = $input.attr('name');

        data[name] = value;

      }

      // do any client side validation. return false if there's probs
      var valid = on_validate(data);

      if (valid !== true) {

        var err_message = valid.err_message || "form invalid";

        console.error(err_message);

        return;

      }

      on_send($this);

      // add a class to form if request is not fulfilled in half a second
      // this could do anything from adding 'loading', or animated dots. it's
      // really up to CSS to implement that
      var sent_timeout = window.setTimeout(function () {

        $this.addClass('waiting');

      }, 500);

      api_endpoint({
        url   : action,
        method: method,
        data  : data
      })
      .then(function (result) {
        
        // request fulfilled, don't add 'waiting' class
        window.clearTimeout(sent_timeout);

        // remove waiting class if we've added it
        $this.removeClass('waiting');

        // handle result
        on_result(result);

        // add the finished class. could put 'finished' inside
        // of form. could add an animated check mark icon. This
        // is really up to the CSS styling
        $this.addClass("finished");

        window.setTimeout(function () {

          // remove after three seconds
          $this.removeClass('finished');

        }, 3000);

      })
      .catch(function (error) {
        
        on_error(error);

        // add the 'error' class. could put 'error' inside
        // of form. could add an animated X or demons. This
        // is really up to the CSS styling
        $this.addClass('error');

        window.setTimeout(function () {

          // remove after three seconds
          $this.removeClass('error');

        }, 3000);
      
      });

    });

    return this;

  }

})();

(function () {

  var api_endpoint = app.api_endpoint;

  // an aggregate is just an ajaxified box with records.
  // will allow for pagination
  $.fn.aggregate = function (configs) {

    configs = configs || {};

    var $this = $(this);

    var source, params; 

    source      = configs.source || null;
    params      = configs.params || {};

    var on_load, record_template, no_record_msg;

    record_template = configs.record_template || function () { return $("<div>"); };
    no_record_msg   = "<p>Nothing available at this time</p>";

    on_load = configs.on_load || function (results) {

      results = results || [];

      $this.empty();

      if (!results.length) {
        $this.append((typeof no_record_msg === "function"? no_record_msg(): no_record_msg));
      }

      console.log(results);
      // else, loop through found results
      for (var i = 0; i < results.length; i++) {

        // take data from results and pass into record template function
        var data = results[i];

        var $record = record_template(data); 

        // append record template to $this
        $this.append($record); 

      }
        
    };

    pagination  = configs.pagination  || false;

    if (pagination) {
      on_paginate = configs.on_paginate || function () {};
      on_next     = configs.on_next     || function () {};
      on_prev     = configs.on_prev     || function () {};
    }

    function reload_records(data) {

      // allow data to be injected from elsewhere
      data = data || null;

      if (data !== null) {

        on_load(data);

        return;

      }

      console.log(source, params);
      if (source === null)
        return;


      // otherwise, try sending AJAX request to source 
      // specified with parameters, then use the on_load
      // event handler
     
      // TODO: get pagination keys. pass into data
      api_endpoint({
        url: source,
        method: "GET",
        data: (typeof params === "function" ? params() : params)
      })
      .then(on_load)
      .catch(function (error) {

        console.error(error); 

      });

    }

    // initial resource loading
    reload_records();

    // todo: bind events to paginators (if enabled)
    
    this.reload_records = reload_records;

    return $(this);

  };

})();

(function () {

  $.fn.image_loader = function (configs) {

    configs = configs || {};

    // max size of 15mb? change?
    max_size = configs.max_size || 15000000;

    // min 5kb. too small? do we need a minimum
    min_size = configs.min_size || 5000;

    // allow no more than 12 images
    max_images = configs.max_images || 12;

    // assume that we want these kinds of images. allow overwriting though
    accept = configs.accept || ["image/jpg", "image/jpeg", "image/png"];

    var $file_input = $(this);

    if (!$file_input.is('input') || $file_input.attr('type') != 'file' ) {
      console.error('image_loader can only be used on input'); 
    }

    var name = $file_input.attr('name');

    var $label = $('label[for=' + name + ']');

    var $wrapper = $('<div>').attr({class: 'image-loader-wrapper'});

    var $display = $('<div>').attr({class: 'image-loader-display'});

    function image_template (data) {

      var $img_wrapper = $('<div>').attr({class: "image-wrapper"});

      var $img = $('<img>');

      var reader = new FileReader();

      reader.onload = function (e) {

        $img.attr('src', e.target.result) 

      };

      reader.readAsDataURL(data);

      $img_wrapper.append($('<div>').append($img));

      return $img_wrapper;

    } 

    // code re-use! woo
    $display.aggregate({
      record_template: image_template,
      no_record_msg: "<p>No images</p>"
    });

    // bind event on label (which takes effect as new
    // input button. A little CSS is used as well)
    $label.click(function () {

      // proxy clicks to the hidden file input
      $file_input.click();

    });

    function show_error (message) {
       
      console.error(message);

      var $err_msg = $('<div>').attr({class:"form-prompt error"});

      $err_msg.text(message);

      $label.after($err_msg);

      window.setTimeout(function () {

        $err_msg.fadeOut(3000, $err_msg.remove);

      }, 5000);

    }

    function display_accept() {

      return accept.map(function (type) {

        return '.' + type.split('/')[1];

      }).join(' ');

    }

    function display_bytes(bytes) {

      if (bytes >= 1000000) {

        return (bytes / 1000000) + "mb";

      }

      return (bytes / 1000) + "kb";

    }

    // event handler for when the input is changed
    // (in effect, when the files are selected from dialogue
    // and 'ok' is clicked)
    $file_input.change(function () {

      // get FileList
      var files = $file_input.prop('files');

      if (files.length > max_images) {

        show_error([
          "A maximum of " + max_images + " is allowed.",
          "You have chosen " + files.length + ".",
        ].join(" "));

        return;

      }

      console.log(files);

      // add an 'index' to each file. also validate each one
      for (var index = 0; index < files.length; index++) {

        var file = files[index];

        file.index = index;

        // not an accepted file
        if (accept.indexOf(file.type) == -1) {

          show_error(file.name + " is not of a supported type");

          return;

        }

        if (file.size > max_size) {

          show_error([
            file.name + " is too large, max. size is ",
            display_bytes(max_size) + ". " + file.name,
            "is " + display_bytes(file.size) + "."
          ].join(" "));

          return;

        }

      }

      // tell the display to reload, using files as data
      // see 'aggregate.js' for more info on aggregates
      $display.reload_records(files);
    
    });

    var $helper  = $('<div>').attr({class:"form-prompt"});

    $helper.text([
      "A maximum of " + max_images + " is allowed. Supported types are",
      display_accept() + ". each file must be under",
      display_bytes(max_size) + "."
    ].join(" "));

    // wrapp the display and input
    $file_input.wrap($wrapper);
    $file_input.before($display);
    $file_input.after($label);
    $label.after($helper);

    return $file_input;

  };

})();

////// TEMPLATES //////
// what goes here? anything that is generally presentational
// like a type of record on a page. If your widget morso extends
// functionality, consider putting it in its own file (like ajaxify,
// aggregate, and image_loader)
(function () {

  // fields for displaying records
  function field (data) {

    var $field, $wrapper, $label;

    var name, value, has_label, label;

    name        = data.name   || "";
    value       = data.value  || "";
    field_class = data.field_class  || "";

    has_label = data.has_label === false ? false: true; 

    $wrapper = $('<div>').attr({
      class: "field-wrapper " + name
    });

    if (has_label) {

      label = data.label || name.replace("_", ' ');

      $label = $('<span>').attr({
        class: "label " + name
      }).text(label);

      $wrapper.append($label);

    }

    $field = $('<span>').attr({
      class: ["field", name, field_class].join(' ')
    }).text(value);

    $wrapper.append($field);

    return $wrapper;

  }

  function modal (data) {

    var message = data.message || "";

    var on_confirm, on_cancel;

    on_confirm = data.on_confirm || function () { };
    on_cancel  = data.on_cancel  || null;

    var confirm_text, cancel_text;

    confirm_text = data.confirm_text || "Ok";
    cancel_text  = data.cancel_text  || "Cancel";

    $modal = $('<div>').attr({
      class: ['modal', modal_class].join(" ")
    });

    $message = $('<div>').text(message);

    $confirm = $('<button class="confirm">').text(confirm_text);

    $confirm.on_click(function () {

      $modal.addClass('finished');

      on_confirm();

      window.setTimeout(function() {

        $modal.remove();

      }, 3000);

    });

    $modal.append($message, $confirm);

    if (on_cancel) {

      $cancel  = $('<button class="cancel">').text(cancel_text);

      $cancel.on_click(function () {

        $modal.addClass('finished');

        on_cancel();

        window.setTimeout(function() {

          $modal.remove();

        }, 3000);

      });

      $modal.setTimeout(function() {

        $modal.addClass('loaded');

      }, 0);

      $modal.append($cancel);

    }

    return $modal;

  } 

  function listing (data) {

    var $listing = $('<div class="record listing">');

    var $title, $link, $created, $ask;

    $title = field({name: 'title', value: data.title, has_label: false}); 

    $link  = $('<a>').attr({
      href: app.site_root() + "/listing/" + data.id
    });

    $link.append($title);

    var types = {
      'auction': 'Auction',
      'buy_now': 'Buy Now'
    };

    $type = field({name: 'type', value: types[data.type], has_label: false});

    // pro tip, prefixing a string with + coerces string
    // to number in javascript. this must be done here
    // because "0" is truthy in javascript, while 0 is not
    var currency = +data.bitcoin ? "bitcoin" : "dollars";

    data.ask = +data.ask;

    if (currency == "dollars") 
      data.ask = data.ask.toFixed(2);

    ask_labels = {"auction": "Ask", "buy_now": "Price"};

    $ask = field({name: 'ask', label: ask_labels[data.type], value: data.ask, field_class: currency});


    var statuses = {
      "active": "Available",
      "sold"  : "Sold"
    };

    var $status = field({
      name: "status",
      value: statuses[data.status],
      css_class: data.status
    });

    var date_format = app.date_format_short();


    var start = moment(data.start).format(date_format);

    var has_started = moment(data.start).isSameOrBefore(moment(new Date()));

    var start_label_text = has_started ? "started" : "starts";

    var $start = field({name: 'start', label: start_label_text, value: start});


    var end = moment(data.end).format(date_format);

    var has_ended   = moment(data.end).isSameOrBefore(moment(new Date()));

    var end_label_text = has_ended ? "ended" : "ends";

    var $end = field({name: 'end', label: end_label_text, value: end});

    $listing.append(
      $link,
      $ask,
      $status,
      $start,
      $end,
      $type
    );

    return $listing;

  }

  app.templates = {
    field  : field,
    modal  : modal,
    listing: listing
  };

})();

(function () {

  $(app.bind_controllers);

})();

////// LISTING CONTROLLERS //////
// html forms do not support PUT and DELETE (I was surprised)
// AJAX however, does support these verbs. our edit forms will then
// use AJAX to follow the REST specification as best as possible
// POST is supported, and there is no problem doing a simple server side
// redirect

//// View Listing ////
app.controller("view-listing", function ($elem) {

  var $bid_aggregate = $('.aggregate.bid');

  $bid_aggregate.aggregate({
    no_record_msg: "No one has placed a bid yet"
  });

});

app.controller("create-listing", function ($elem) {

  var $form = $('form.create-listing', $elem);

  var $image_loader = $('input.image-loader', $form);

  $image_loader.image_loader();

});

//// Edit Listing Form ////
app.controller("update-listing-form", function ($elem) {

  var modal = app.templates.modal;

  var $form = $('form.update-listing', $elem);

  function handle_results (result) {

    // look for success
    if (result.success)
      window.location = app.site_root() + "/listing/" + result.id;
    
    // TODO: give message
    // give message or redirect
    $('body').append(modal({
      message: result.errors.pop() 
    }));

  }

  // must ajaxify the edit form to honor "PUT" method
  $form.ajaxify({
    on_result: handle_results
  });

});

//// Delete Listing Form ////
app.controller("delete-listing-form", function ($elem) {

  var $form = $('form.delete-listing', $elem);

  function handle_results (result) {

    if (result.success) {

      window.location = app.site_root() + "/account";

      return;

    }

    // TODO: handle error/ show error

  }

  $form.ajaxify({
    on_result: handle_results
  });

});

//// Listing Search ////
app.controller('listing-search', function ($elem) {

  var listing_template = app.templates.listing;

  var listing_aggregate = $('.aggregate.listing', $elem);

  // TODO: expose some interface to aggregates to allow re-loading
  var search_form = $('form.listing-search', $elem);

  var initial_values = {};

  // get initial values from form if the form input is cached on a page refresh
  $('input', search_form).not('input[type=submit]').each(function (index, elem) {

    console.log(elem);

    var $elem = $(elem); 

    var name, value;
    name  = $elem.attr('name');
    value = $elem.val();

    initial_values[name] = value;

  });

  // creates aggregate object. load records with initial form query values
  listing_aggregate.aggregate({
    source: "/listing/search",
    params: initial_values,
    record_template: listing_template
  });

  // ajaxify form
  search_form.ajaxify({
    // functions, beautiful functions
    // simply call reload_records on the aggregate
    // when data comes back
    on_result: listing_aggregate.reload_records
  });

  // bind auto-submit handlers
  function auto_submit () {

    search_form.submit();

  }

  var $keyword, $start, $end;

  $keyword = $('input.keyword', search_form);

  // variable set here for lexical scoping magic
  var keyword_timeout;

  // fire event when key goes up on keyword focus
  $keyword.keyup(function () {

    // clear the timeout if it exists. basically,
    // don't keep auto-submitting if the user presses
    // a key faster than 1 key per second
    window.clearTimeout(keyword_timeout);

    // set a timeout, submit form after 1 second
    keyword_timeout = window.setTimeout(function () {

      auto_submit();

    }, 1000);

  });

  // auto submit when the date is changed
  $start = $('input.start', search_form);
  $start.change(auto_submit);

  $end = $('input.end', search_form);
  $end.change(auto_submit);

});

app.controller('home-page', function ($elem) {

  var listing_template = app.templates.listing;

  var recently_sold_aggregate = $('.aggregate.recently-sold', $elem);

  var today, one_week_out;
  today = moment(new Date());
  one_week_out = moment(new Date()).add(7, 'days');

  var date_format = app.date_format(); 

  recently_sold_aggregate.aggregate({
    source: "/listing/search",
    params: {
      start: today.format(date_format),
      end  : one_week_out.format(date_format),
      limit: 50,
      status: "sold"
    },
    record_template: listing_template
  });

  var new_listing_aggregate = $('.aggregate.new-listing', $elem);

  new_listing_aggregate.aggregate({
    source: "/listing/search",
    params: {
      start: today.format(date_format),
      end  : one_week_out.format(date_format),
      limit: 50,
      status: "active"
    },
    record_template: listing_template
  });

});

////// USER FORMS //////
// html forms do not support PUT and DELETE (I was surprised)
// AJAX however, does support these verbs. our edit forms will then
// use AJAX to follow the REST specification as best as possible
app.controller("user-edit-form", function ($form) {

  function handle_results (result) {

  }

  $form.ajaxify({
    on_result: handle_results
  });

});

app.controller("user-delete-form", function ($form) {

  function handle_results (result) {

    if (result.success) {

      // flash message should be set server side. user should be logged out.
      // just redirect to home page
      window.location = app.site_root(); 

    }

  }

  $form.ajaxify({
    on_result: handle_results
  });

});

// controller for users account
app.controller('user-profile', function ($elem) {

  var listing_template = app.templates.listing;

  var recently_sold_aggregate;

  recently_sold_aggregate = $('.aggregate.recently-sold', $elem);

  user_listings_aggregate = $('.aggregate.user-created.listing', $elem);

  var seller_id = user_listings_aggregate.attr('data-user');

  var date_format = app.date_format();

  user_listings_aggregate.aggregate({
    source: "/listing/search",
    // get listings from this user from start of the EPOCH
    params: {seller_id: seller_id, start: moment(new Date(0)).format(date_format)},
    record_template: listing_template
  });

});

// controller for users account
app.controller('my-account', function ($elem) {

  // bought should only be visible from my account
  recently_bought_aggregate = $('aggregate.recently-bought', $elem);

});
