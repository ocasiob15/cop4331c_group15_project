////// TEMPLATES //////
// what goes here? anything that is generally presentational
// like a type of record on a page. If your widget morso extends
// functionality, consider putting it in its own file (like ajaxify,
// aggregate, and image_loader)
(function () {

  // fields for displaying records
  function field (data) {

    var $field, $wrapper, $label;

    var name, value, has_label, label;

    name        = data.name   || "";
    value       = data.value  || "";
    field_class = data.field_class  || "";

    has_label = data.has_label === false ? false: true; 

    $wrapper = $('<div>').attr({
      class: "field-wrapper " + name
    });

    if (has_label) {

      label = data.label || name.replace("_", ' ');

      $label = $('<span>').attr({
        class: "label " + name
      }).text(label);

      $wrapper.append($label);

    }

    $field = $('<span>').attr({
      class: ["field", name, field_class].join(' ')
    }).text(value);

    $wrapper.append($field);

    return $wrapper;

  }

  function modal (data) {

    var message = data.message || "";

    var on_confirm, on_cancel;

    on_confirm = data.on_confirm || function () { };
    on_cancel  = data.on_cancel  || null;

    var confirm_text, cancel_text;

    confirm_text = data.confirm_text || "Ok";
    cancel_text  = data.cancel_text  || "Cancel";

    $modal = $('<div>').attr({
      class: ['modal', modal_class].join(" ")
    });

    $message = $('<div>').text(message);

    $confirm = $('<button class="confirm">').text(confirm_text);

    $confirm.on_click(function () {

      $modal.addClass('finished');

      on_confirm();

      window.setTimeout(function() {

        $modal.remove();

      }, 3000);

    });

    $modal.append($message, $confirm);

    if (on_cancel) {

      $cancel  = $('<button class="cancel">').text(cancel_text);

      $cancel.on_click(function () {

        $modal.addClass('finished');

        on_cancel();

        window.setTimeout(function() {

          $modal.remove();

        }, 3000);

      });

      $modal.setTimeout(function() {

        $modal.addClass('loaded');

      }, 0);

      $modal.append($cancel);

    }

    return $modal;

  } 

  function listing (data) {

    var $listing = $('<div class="record listing">');

    var $title, $link, $created, $ask;

    $title = field({name: 'title', value: data.title, has_label: false}); 

    $link  = $('<a>').attr({
      href: app.site_root() + "/listing/" + data.id
    });

    $link.append($title);

    var types = {
      'auction': 'Auction',
      'buy_now': 'Buy Now'
    };

    $type = field({name: 'type', value: types[data.type], has_label: false});

    // pro tip, prefixing a string with + coerces string
    // to number in javascript. this must be done here
    // because "0" is truthy in javascript, while 0 is not
    var currency = +data.bitcoin ? "bitcoin" : "dollars";

    data.ask = +data.ask;

    if (currency == "dollars") 
      data.ask = data.ask.toFixed(2);

    ask_labels = {"auction": "Ask", "buy_now": "Price"};

    $ask = field({name: 'ask', label: ask_labels[data.type], value: data.ask, field_class: currency});


    var statuses = {
      "active": "Available",
      "sold"  : "Sold"
    };

    var $status = field({
      name: "status",
      value: statuses[data.status],
      css_class: data.status
    });

    var date_format = app.date_format_short();


    var start = moment(data.start).format(date_format);

    var has_started = moment(data.start).isSameOrBefore(moment(new Date()));

    var start_label_text = has_started ? "started" : "starts";

    var $start = field({name: 'start', label: start_label_text, value: start});


    var end = moment(data.end).format(date_format);

    var has_ended   = moment(data.end).isSameOrBefore(moment(new Date()));

    var end_label_text = has_ended ? "ended" : "ends";

    var $end = field({name: 'end', label: end_label_text, value: end});

    $listing.append(
      $link,
      $ask,
      $status,
      $start,
      $end,
      $type
    );

    return $listing;

  }

  app.templates = {
    field  : field,
    modal  : modal,
    listing: listing
  };

})();
