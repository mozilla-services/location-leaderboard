module.exports = function(grunt) {

    grunt.initConfig({
        less: {
            sandstone: {
                files: {
                    'css/sandstone/sandstone-resp.css' : 'css/sandstone/sandstone-resp.less'
                }
            },
            sandstone_prod: {
                options: {
                    compress: true
                },
                files: {
                    'css/sandstone/sandstone-resp.min.css' : 'css/sandstone/sandstone-resp.less'
                }
            }
        },
        jshint: {
            files: ['grunt.js', 'js/*.js'],
            options: {
                bitwise: true,
                camelcase: true,
                curly: true,
                eqeqeq: true,
                forin: true,
                immed: true,
                latedef: true,
                newcap: true,
                noarg: true,
                quotmark: "single",
                regexp: true,
                undef: true,
                unused: true,
                trailing: true,
                browser: true,
                jquery: true
            }
        },
        csslint: {
            base_theme: {
                src: "css/*.css",
                rules: {
                    "empty-rules": 2,
                    "fallback-colors": 2,
                    "font-sizes": 2,
                    "important": 2,
                    "outline-none": 2,
                    "vendor-prefix": 2,
                    "zero-units": 2
                }
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-jshint')
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-css');

    grunt.registerTask('default', 'less:sandstone');
    grunt.registerTask('lintify', ['jshint', 'csslint']);
    grunt.registerTask('prep_prod', 'less:sandstone lintify less:sandstone_prod');
};
