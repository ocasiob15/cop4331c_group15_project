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
