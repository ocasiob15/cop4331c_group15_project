app.controller('payment-form', function ($elem) {

  var $form = $('form.payment', $elem);

  // ajaxify the form
  $form.ajaxify({
    on_result: function (result) {

      if (!result.success) {

        // TODO: handle result.errors and put on page
        console.error(result);
        return;

      }

      window.location = result.redirect;

    }
  });

  // give checkbox functionality to set shipping based on billing
  var $same_as_billing = $('input#same_as_billing', $form);

  // billing fields
  var $bill_street, $bill_city, $bill_state, $bill_zip;

  $bill_street = $('input#billing_street');
  $bill_city   = $('input#billing_city');
  $bill_state  = $('input#billing_state');
  $bill_zip    = $('input#billing_zip');
  

  // shipping fields
  var $ship_street, $ship_city, $ship_state, $ship_zip;

  $ship_street = $('input#shipping_street');
  $ship_city   = $('input#shipping_city');
  $ship_state  = $('input#shipping_state');
  $ship_zip    = $('input#shipping_zip');


  function copy_billing () {

    var same = $same_as_billing[0].checked;

    if (same) {

      $ship_street.val($bill_street.val());
      $ship_city.val($bill_city.val());
      $ship_state.val($bill_state.val());
      $ship_zip.val($bill_zip.val());

      return;

    }

    // otherwise set to blank
    $ship_street.val('');
    $ship_city.val('');
    $ship_state.val('');
    $ship_zip.val('');

  } 

  $same_as_billing.change(copy_billing);

});
