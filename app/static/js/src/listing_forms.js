////// LISTING FORMS //////
// html forms do not support PUT and DELETE (I was surprised)
// AJAX however, does support these verbs. our edit forms will then
// use AJAX to follow the REST specification as best as possible
app.controller("listing-edit-form", function ($form) {

  function handle_results () {

  }

  $form.ajaxify({
    on_result: handle_results
  });

});

app.controller("listing-delete-form", function ($form) {

  function handle_results () {

  }

  $form.ajaxify({
    on_result: handle_results
  });

});
