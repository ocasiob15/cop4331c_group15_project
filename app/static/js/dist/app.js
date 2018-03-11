(function () {

  window.app = window.app || {};

  app.api_endpoint = function (options) {

    options = options         || {};
    options.url = options.url || "";

    options.url = app.site_root() + options.url;

    // override anything else necessary

    // return promisified request
    return $.ajax(options);

  }

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

  $(function () {

    bind_controllers();

  });
 
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

      console.log(results); 

      if (!results) {
        $this.append((typeof no_record_msg === "function"? no_record_msg(): no_record_msg));
      }

      // else, loop through found results

        // take data from results and pass into record template function
        
        // append record template to $this
        
    };

    pagination  = configs.pagination  || false;

    if (pagination) {
      on_paginate = configs.on_paginate || function () {};
      on_next     = configs.on_next     || function () {};
      on_prev     = configs.on_prev     || function () {};
    }

    function reload_records() {

      // todo, get pagination keys. pass into data

      api_endpoint({
        url: source,
        method: "GET",
        data: (typeof params === "function" ? params() : params)
      })
      .then(on_load);

    }

    // initial resource loading
    reload_records();

    // todo: bind events to paginators (if enabled)

  };

})();

(function () {

  var api = app.api_endpoint;
  
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
        $this.addClass('finished');

        window.setTimeout(function () {

          // remove after three seconds
          $this.removeClass('finished');

        }, 3000)

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

        }, 3000)
      
      });

    });

  }

})(app)

////// LISTING FORMS //////
// html forms do not support PUT and DELETE (I was surprised)
// AJAX however, does support these verbs. our edit forms will then
// use AJAX to follow the REST specification as best as possible
app.controller("listing-edit-form", function ($form) {

  function handle_results () {

  }

  $form.ajaxify({
    on_result: handle_results
  });

});

app.controller("listing-delete-form", function ($form) {

  function handle_results () {

  }

  $form.ajaxify({
    on_result: handle_results
  });

});

////// USER FORMS //////
// html forms do not support PUT and DELETE (I was surprised)
// AJAX however, does support these verbs. our edit forms will then
// use AJAX to follow the REST specification as best as possible
app.controller("user-edit-form", function ($form) {

  function handle_results (result) {

    console.log(result);

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

  var recently_sold_aggregate;

  recently_sold_aggregate = $('.aggregate.recently-sold', $elem);

  user_listings_aggregate = $('.aggregate.user-listing', $elem);

});

// controller for users account
app.controller('my-account', function ($elem) {

  // bought should only be visible from my account
  recently_bought_aggregate = $('aggregate.recently-bought', $elem);

});
