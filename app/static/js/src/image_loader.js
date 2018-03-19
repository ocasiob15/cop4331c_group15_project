(function () {

  $.fn.image_loader = function (configs) {

    configs = configs || {};

    // max size of 15mb? change?
    max_size = configs.max_size || 15000000;

    // min 5kb. too small? do we need a minimum
    min_size = configs.min_size || 5000;

    // allow no more than 12 images
    max_images = configs.max_images || 12;

    // assume that we want these kinds of images. allow overwriting though
    accept = configs.accept || ["image/jpg", "image/jpeg", "image/png"];

    var $file_input = $(this);

    if (!$file_input.is('input') || $file_input.attr('type') != 'file' ) {
      console.error('image_loader can only be used on input'); 
    }

    var name = $file_input.attr('name');

    var $label = $('label[for=' + name + ']');

    var $wrapper = $('<div>').attr({class: 'image-loader-wrapper'});

    var $display = $('<div>').attr({class: 'image-loader-display'});

    function image_template (data) {

      var $img_wrapper = $('<div>').attr({class: "image-wrapper"});

      var $img = $('<img>');

      var reader = new FileReader();

      reader.onload = function (e) {

        $img.attr('src', e.target.result) 

      };

      reader.readAsDataURL(data);

      $img_wrapper.append($('<div>').append($img));

      return $img_wrapper;

    } 

    // code re-use! woo
    $display.aggregate({
      record_template: image_template,
      no_record_msg: "<p>No images</p>"
    });

    // bind event on label (which takes effect as new
    // input button. A little CSS is used as well)
    $label.click(function () {

      // proxy clicks to the hidden file input
      $file_input.click();

    });

    function show_error (message) {
       
      console.error(message);

      var $err_msg = $('<div>').attr({class:"form-prompt error"});

      $err_msg.text(message);

      $label.after($err_msg);

      window.setTimeout(function () {

        $err_msg.fadeOut(3000, $err_msg.remove);

      }, 5000);

    }

    function display_accept() {

      return accept.map(function (type) {

        return '.' + type.split('/')[1];

      }).join(' ');

    }

    function display_bytes(bytes) {

      if (bytes >= 1000000) {

        return (bytes / 1000000) + "mb";

      }

      return (bytes / 1000) + "kb";

    }

    // event handler for when the input is changed
    // (in effect, when the files are selected from dialogue
    // and 'ok' is clicked)
    $file_input.change(function () {

      // get FileList
      var files = $file_input.prop('files');

      if (files.length > max_images) {

        show_error([
          "A maximum of " + max_images + " is allowed.",
          "You have chosen " + files.length + ".",
        ].join(" "));

        return;

      }

      console.log(files);

      // add an 'index' to each file. also validate each one
      for (var index = 0; index < files.length; index++) {

        var file = files[index];

        file.index = index;

        // not an accepted file
        if (accept.indexOf(file.type) == -1) {

          show_error(file.name + " is not of a supported type");

          return;

        }

        if (file.size > max_size) {

          show_error([
            file.name + " is too large, max. size is ",
            display_bytes(max_size) + ". " + file.name,
            "is " + display_bytes(file.size) + "."
          ].join(" "));

          return;

        }

      }

      // tell the display to reload, using files as data
      // see 'aggregate.js' for more info on aggregates
      $display.reload_records(files);
    
    });

    var $helper  = $('<div>').attr({class:"form-prompt"});

    $helper.text([
      "A maximum of " + max_images + " is allowed. Supported types are",
      display_accept() + ". each file must be under",
      display_bytes(max_size) + "."
    ].join(" "));

    // wrapp the display and input
    $file_input.wrap($wrapper);
    $file_input.before($display);
    $file_input.after($label);
    $label.after($helper);

    return $file_input;

  };

})();
