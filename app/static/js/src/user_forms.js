////// USER FORMS //////
// html forms do not support PUT and DELETE (I was surprised)
// AJAX however, does support these verbs. our edit forms will then
// use AJAX to follow the REST specification as best as possible
app.controller("user-edit-form", function ($form) {

  function handle_results (result) {

    console.log(result);

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
