// Include gulp
var gulp = require('gulp'),
    merge = require('merge-stream'),
    less = require('gulp-less');

var less_paths = [
    './leaderboard/static/less/*.less',
    './leaderboard/static/sandstone/less/*.less'
];

// Compile Our Less
gulp.task('less', function() {
    var tasks = less_paths.map(function (path) {
        return gulp.src(path)
            .pipe(less())
            .pipe(gulp.dest('./leaderboard/static/css/'));
    });

    return merge(tasks);
});

// Watch Files For Changes
gulp.task('watch', function() {
    less_paths.map(function (path) {
        gulp.watch(path, ['less']);
    });
});

// Default Task
gulp.task('default', ['less', 'watch']);
