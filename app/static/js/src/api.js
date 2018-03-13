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
