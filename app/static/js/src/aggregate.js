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
