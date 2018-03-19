app.controller('home-page', function ($elem) {

  var listing_template = app.templates.listing;

  var recently_sold_aggregate = $('.aggregate.recently-sold', $elem);

  var today, one_week_out;
  today = moment(new Date());
  one_week_out = moment(new Date()).add(7, 'days');

  var date_format = app.date_format(); 

  recently_sold_aggregate.aggregate({
    source: "/listing/search",
    params: {
      start: today.format(date_format),
      end  : one_week_out.format(date_format),
      limit: 50,
      status: "sold"
    },
    record_template: listing_template
  });

  var new_listing_aggregate = $('.aggregate.new-listing', $elem);

  new_listing_aggregate.aggregate({
    source: "/listing/search",
    params: {
      start: today.format(date_format),
      end  : one_week_out.format(date_format),
      limit: 50,
      status: "active"
    },
    record_template: listing_template
  });

});
