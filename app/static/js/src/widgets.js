app.controller('countdown', function ($elem) {

  var start = moment($elem.attr('data-start'));

  var end   = moment($elem.attr('data-end'));

  $elem.text(start.diff(end));

});
