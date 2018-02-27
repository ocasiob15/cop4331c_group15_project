const 
  gulp = require("gulp"),
  gutil = require("gulp-util"),
  concat = require("gulp-concat"),
  uglify = require("gulp-uglify"),
  less = require("gulp-less"),
  min = require("gulp-clean-css"),
  print = require("gulp-print"),
  order = require('gulp-order'),
  plumber = require("gulp-plumber");
   
// watch javascript files in the 'src' directory.
// concat and uglify into dist. do not include
// files under lib. these may be minified already
// which causes problems with gulp-uglify
gulp.task("js", function () {
  var sources = [
    'js/src/*.js'
  ];
  return gulp.watch("js/src/*js", function () {
    // src
    gulp.src(sources)
      .pipe(order([
        'app.js',
        '*.js'
      ]))
      .pipe(plumber())
      .pipe(concat("app.js"))
      .pipe(gulp.dest("js/dist/"))
      .pipe(concat("app.min.js"))
      .pipe(uglify())
      .on('error', gutil.log)
      .pipe(gulp.dest("js/dist/"));
         
 }); 
});


// watch less files and compile into CSS
gulp.task("css", function () {
  return gulp.watch("style/less/*.less", function () {
    gulp.src("style/less/*.less")
      .pipe(plumber())
      .pipe(less())
      .pipe(concat("main.css"))
      .pipe(min())
      .pipe(gulp.dest("style/css/"));
  });
});


gulp.task("default", ["js", "css"]);
