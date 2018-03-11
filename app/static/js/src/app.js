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
