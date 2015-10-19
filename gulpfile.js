// Include gulp
var gulp = require('gulp'),
    gutil = require('gulp-util'),
    shell = require('gulp-shell'),
    merge = require('merge-stream'),
    less = require('gulp-less'),
    reactify = require('reactify'),
    browserify = require('gulp-browserify');

var collectstatic = 'python manage.py collectstatic --noinput | tail -n 1'

var sandstone_less_path = './leaderboard/sandstone/static/sandstone/less/*.less';
var leaderboard_less_path = './leaderboard/static/less/*.less';
var js_path = './leaderboard/static/js/*.js';

// Compile Our Less
function less_task (name, input_paths, output_path) {
  gulp.task(name, function() {
    var tasks = input_paths.map(function (input_path) {
      // Crazy recipe from
      // https://github.com/gulpjs/gulp/issues/71
      var less_task = less();
      less_task.on('error', function (e) {
        gutil.log(e);
        less_task.end();
      });
      return gulp.src(input_path)
        .pipe(less_task)
        .pipe(gulp.dest(output_path))
        .pipe(shell([collectstatic]));
    });

    return merge(tasks);
  });
}

less_task('less-sandstone', [sandstone_less_path], './leaderboard/sandstone/static/sandstone/css/');
less_task('less-leaderboard', [leaderboard_less_path], './leaderboard/static/css/');

// Basic usage 
gulp.task('scripts', function() {
  // Single entry point to browserify 
  gulp.src('./leaderboard/static/js/leaderboard.js')
    .pipe(
      browserify({
        transform: [reactify],
        insertGlobals : true,
        standalone: 'leaderboard'
      }).on('error', gutil.log))
    .pipe(gulp.dest('./leaderboard/static/js/build/'))
    .pipe(shell([collectstatic]));
});

// Watch Files For Changes
gulp.task('watch', function() {
  [
    ['less-sandstone', sandstone_less_path], 
    ['less-leaderboard', leaderboard_less_path],
    ['scripts', js_path],
  ].map(function (task) {
    var task_name = task[0];
    var task_path = task[1];
    return gulp.watch(task_path, [task_name]);
  });
});

// Default Task
gulp.task('default', ['watch']);
