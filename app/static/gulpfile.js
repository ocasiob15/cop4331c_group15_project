const 
  gulp    = require("gulp"),
  concat  = require("gulp-concat"),
  uglify  = require("gulp-uglify"),
  less    = require("gulp-less"),
  min     = require("gulp-minify-css"),
  print   = require("gulp-print"),
  order   = require('gulp-order'),
  plumber = require("gulp-plumber");
   
// watch javascript files in the 'src' directory.
// concat and uglify into dist. do not include
// files under lib. these may be minified already
// which causes problems with gulp-uglify
gulp.task("js", function () {
  var sources = [
    './js/src/*.js'
  ];
  return gulp.watch("./js/src/**/*.js").on('change', function () {
    // src
    gulp.src(sources)
      .pipe(order([
        'api.js',
        'controller.js',
        'ajaxify.js',
        'aggregate.js',
        'image_loader.js',
        'templates.js',
        '*.js',
        'app.js'
      ]))
      .pipe(plumber())
      .pipe(concat("app.js"))
      .pipe(gulp.dest("js/dist/"))
      .pipe(concat("app.min.js"))
      .pipe(uglify())
      .pipe(gulp.dest("js/dist"))
 }); 
});

gulp.task("less", function () {

  return gulp.src("./style/less/*.less")
    .pipe(plumber())
    .pipe(concat("main.css"))
    .pipe(less())
    .pipe(min())
    .pipe(gulp.dest("style/css"));

});

// watch less files and compile into CSS
gulp.task("css", function () {
  return gulp.watch('./style/less/*.less', ['less']);
});


gulp.task("default", ["js", "css"]);

