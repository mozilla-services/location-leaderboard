// Include gulp
var gulp = require('gulp'),
  merge = require('merge-stream'),
  less = require('gulp-less'),
  browserify = require('gulp-browserify');


var sandstone_less_path = './leaderboard/sandstone/static/sandstone/less/*.less';
var leaderboard_less_path = './leaderboard/static/less/*.less';
var js_path = './leaderboard/static/js/*.js';

// Compile Our Less
function less_task (name, input_paths, output_path) {
  gulp.task(name, function() {
    var tasks = input_paths.map(function (input_path) {
      return gulp.src(input_path)
        .pipe(less())
        .pipe(gulp.dest(output_path));
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
    .pipe(browserify({
      insertGlobals : true,
      standalone: 'leaderboard'
    }))
    .pipe(gulp.dest('./leaderboard/static/js/build/'))
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
    gulp.watch(task_path, [task_name]);
  });
});

// Default Task
gulp.task('default', ['watch']);
