(function () {

  var api_endpoint = app.api_endpoint;
  
  // do the thing
  $.fn.ajaxify = function (configs) {

    configs = configs || {};

    var on_validate, on_send, on_result, on_error;

    on_validate = configs.on_validate || function () { return true };
    on_send     = configs.on_send     || function () {};
    on_result   = configs.on_result   || function () {};
    on_error    = configs.on_error    || function () {};

    var $this = $(this);

    if (!$this.is('form')) {

      console.error("ajaxify must be called on a form");

      return

    }

    $this.addClass('ajaxified');

    $this.submit(function (e) {

      e.preventDefault();
      
      var method, action, inputs;

      method = $this.attr('method');
      action = $this.attr('action');

      inputs = $('input,textarea,select', $this)
      inputs = inputs.not('input[type=submit],input[type=radio]:not(:checked),input[type=checkbox]:not(:checked)');

      var data = {};

      for (var i = 0; i < inputs.length; i++) {

        var $input, value, name;

        $input = $(inputs[i]);

        value = $input.val();

        name  = $input.attr('name');

        data[name] = value;

      }

      // do any client side validation. return false if there's probs
      var valid = on_validate(data);

      if (valid !== true) {

        var err_message = valid.err_message || "form invalid";

        console.error(err_message);

        return;

      }

      on_send($this);

      // add a class to form if request is not fulfilled in half a second
      // this could do anything from adding 'loading', or animated dots. it's
      // really up to CSS to implement that
      var sent_timeout = window.setTimeout(function () {

        $this.addClass('waiting');

      }, 500);

      api_endpoint({
        url   : action,
        method: method,
        data  : data
      })
      .then(function (result) {
        
        // request fulfilled, don't add 'waiting' class
        window.clearTimeout(sent_timeout);

        // remove waiting class if we've added it
        $this.removeClass('waiting');

        // handle result
        on_result(result);

        // add the finished class. could put 'finished' inside
        // of form. could add an animated check mark icon. This
        // is really up to the CSS styling
        $this.addClass("finished");

        window.setTimeout(function () {

          // remove after three seconds
          $this.removeClass('finished');

        }, 3000);

      })
      .catch(function (error) {
        
        on_error(error);

        // add the 'error' class. could put 'error' inside
        // of form. could add an animated X or demons. This
        // is really up to the CSS styling
        $this.addClass('error');

        window.setTimeout(function () {

          // remove after three seconds
          $this.removeClass('error');

        }, 3000);
      
      });

    });

    return this;

  }

})();
