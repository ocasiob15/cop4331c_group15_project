// controller for users account
app.controller('user-profile', function ($elem) {

  function listing_template (data) {

    var $listing = $('<div>');

    var $title, $link, $created, $ask;

    $title = $('<div>').attr({
      class:"field title"
    }).text(data.title);

    $link  = $('<a>').attr({
      href: app.site_root() + "/listing/" + data.id
    });

    var type = data.type;

    var currency = Number(data.bitcoin) ? "bitcoin" : "dollars";

    if (currency == "dollars") 
      data.ask = Number(data.ask).toFixed(2);

    $ask_label = $('<span class="label ask">')
    .text(type == "auction" ? "current bid: ": "price: ");

    $ask = $('<span>').attr({
      class: "field ask " + currency
    }).text( + data.ask);

    $link.append($title);

    $listing.append($link, $ask_label, $ask);

    return $listing;

  }

  var recently_sold_aggregate;

  recently_sold_aggregate = $('.aggregate.recently-sold', $elem);

  user_listings_aggregate = $('.aggregate.user-created.listing', $elem);

  var seller_id = user_listings_aggregate.attr('data-user');

  user_listings_aggregate.aggregate({
    source: "/listing/search",
    params: {seller_id: seller_id},
    record_template: listing_template
  });

});

// controller for users account
app.controller('my-account', function ($elem) {

  // bought should only be visible from my account
  recently_bought_aggregate = $('aggregate.recently-bought', $elem);

});
