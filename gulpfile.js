// Include gulp
var gulp = require('gulp'),
    merge = require('merge-stream'),
    less = require('gulp-less');

var sandstone_less_paths = [
    './leaderboard/sandstone/static/sandstone/less/*.less'
];

var leaderboard_less_paths = [
    './leaderboard/static/less/*.less',
];

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

less_task('less-sandstone', sandstone_less_paths, './leaderboard/sandstone/static/sandstone/css/');
less_task('less-leaderboard', leaderboard_less_paths, './leaderboard/static/css/');

// Watch Files For Changes
gulp.task('watch', function() {
    [['less-sandstone', sandstone_less_paths], ['less-leaderboard', leaderboard_less_paths]].map(function (task) {
        var task_name = task[0];
        var task_paths = task[1];
        task_paths.map(function (task_path) {
            gulp.watch(task_path, [task_name]);
        });
    });
});

// Default Task
gulp.task('default', ['less-sandstone', 'less-leaderboard', 'watch']);
