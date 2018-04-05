////// LISTING CONTROLLERS //////
// html forms do not support PUT and DELETE (I was surprised)
// AJAX however, does support these verbs. our edit forms will then
// use AJAX to follow the REST specification as best as possible
// POST is supported, and there is no problem doing a simple server side
// redirect

//// View Listing ////
app.controller("view-listing", function ($elem) {


  /*
  REMOVED: deprected the bid model, which means there is no
  entity to query separate from the listing 
  var $bid_aggregate = $('.aggregate.bid');

  listing_id = $bid_aggregate.attr('data-listing');

  var bid_template = app.templates.bid

  $bid_aggregate.aggregate({
    source: "/listing/" + listing_id + "/bids",
    record_template: bid_template,
    no_record_msg  : "No one has placed a bid yet",
    after_load: function (data) {

      if (!data.length)
        return; 

      var $ask_label = $('h4 > .field.ask', $elem);

      var top_bid = data[0] || {offer: $ask_label.text()};

      $ask_label.text(top_bid.offer);

    }
  });
  */

  // ajaxify the bid placement form if it exists
  $bid_form = $('form.bid.create', $elem);

  var $ask_label = $('h4 > .field.ask', $elem);

  function update_ask (result) {

    if (result.errors || !result.success) {

      var errors = result.errors || {};

      for (var i in errors) {

        var $error = app.templates.error({message: errors[i].pop()});

        $bid_form.prepend($error);

      }

      return;

    }

    var new_ask = result.new_ask;

    $ask_label.text(new_ask);

    // tell the aggregate to reload records from source attribute
    // REMOVED: deprecated bid model
    // $bid_aggregate.reload_records();

  }

  $bid_form.length && (function () {

    $bid_form.ajaxify({
      on_result: update_ask
    });

  })();

  // every 5 seconds, poll the database for bids
  // window.setInterval($bid_aggregate.reload_records, 5000);
  
  // add in a real-time conversion for price to USD
  if ($ask_label.hasClass('bitcoin')) {

    var $conversion = $('<h5>').addClass('conversion');

    var $usd = $('<span class="waiting">');

    window.setInterval(function () {

      $.ajax('https://api.coindesk.com/v1/bpi/currentprice.json')
      .then(function (result) {

        result = result || {};
        result = JSON.parse(result);

        var bpi = result.bpi || {};
        var usd = bpi.USD    || {};

        var rate = usd.rate;
        var rate_num = Number(rate.replace(',', ''));

        var btc = Number($ask_label.text()); 

        $usd.removeClass('waiting');

        $usd.addClass('dollars');

        $usd.text(rate_num * btc);

      });
      
    }, 5000);

    $ask_label.after($conversion);

    $conversion.append("Current price in USD: ", $usd);

  }

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
  $('input,select', search_form).not('input[type=submit]').each(function (index, elem) {

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

  var $keyword, $sort_by, $sort_ord;

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
  $sort_by = $('select.sort_by', search_form);
  $sort_by.change(auto_submit);

  $sort_ord = $('select.sort_ord', search_form);
  $sort_ord.change(auto_submit);

});
