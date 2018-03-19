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
