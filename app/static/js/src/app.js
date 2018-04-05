(function () {

  $(app.bind_controllers);

  // some page loader things
  $(function () {

    // hide flash message after 5 seconds
    window.setTimeout(function () {

       $('.flash-message, .message.error').slideUp();

    }, 5000); 


  });

})();
