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
