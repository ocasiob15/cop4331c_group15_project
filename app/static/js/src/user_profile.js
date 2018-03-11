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
