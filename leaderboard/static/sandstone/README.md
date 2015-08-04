# Sandstone #

A bootstrap for sites in the Mozilla Universe. This project aims to automate as much
of the process of starting a new website using the Mozilla Sandstone theme as possible and,
also provides the tools, via Grunt, to preprocess, lint and minify/uglify the assets.

*NOTE:* For sites based on Django/Playdoh, the Grunt file is not currently included.

# Prerequisites #

You will currently need to following prerequisites installed:

* [Nodejs][nodejs]
* [LESS][less]
* [Volo][volo]

To intall the LESS preprocessor run the following after installing Nodejs

    (sudo) npm install -g less

*Note:* If you are using sandstone for a static website, you will also want:

* [Grunt][grunt]

Install Grunt:

    (sudo) npm install -g grunt

You may be required to use sudo but, in most cases it will be optional.

# Usage #

## For static sites ##

Inside your project's root directory:

    volo add ossreleasefeed/Sandstone#volofile

Once the above has completed, you can add sandstone using the add_sandstone volo target. The
target has two optional arguments:

* folder The folder into which you want sandstone installed [DEFAULT: current directory]
* grunt Whether you want to add Grunt [DEFAULT: false]

    volo add_sandstone folder=target_folder grunt=true

Once completed run:

    npm install

This will install any additional dependencies defined inside package.json. Inside your new project folder
there will also be a .gitignore file that will ensure that the node_modules folder created above, as well
as any .css files will not be included in source control.

Feel free to add any additional exclusions you require.

## For sites based on Playdoh ##

If you have not already, create your project using the following documentation:

http://playdoh.readthedocs.org/en/latest/getting-started/installation.html

Once your Playdoh project has been created, cd into the root using:

    cd projectname

Once inside your project root, run the following command:

    volo add ossreleasefeed/Sandstone/master#volofile

This will add the volofile to your Playdoh project needed to install sandstone in the following step.
Once the above completes, run the following command:

    volo install_sandstone project=yourprojectsname

NOTE: Sandstone no longer assume that you project structure is one of projectname/base so, if your project follows
this convention, you need to call install_sandstone as follows:

volo install_sandstone project=yourprojectsname/base

If you do not specify it as such, the file structure you will end up with will be:

    projectname
    -- css
    -- js
    -- fonts
    -- img
    -- templates/base.html # if you did not specify base=skip

While you wait, volo will do it's magic and grab the latest from the Sandstone repo and then, using the
volofile from before, copy all of the resources you need into the projectname/base/static directory. It
will also add a new base.html template file to your projectname/templates directory you can then extend
to create your template views.

If you have previously run install_sandstone and simply want to update without overwriting you base.html
template, call install_sandstone as follows:

    volo install_sandstone project=yourprojectsname base=skip

When done, the tmp directory will be removed.

### Last step ###

Do something awesome

# Grunt Tasks #

*NOTE:* only avaible to static sites

The current [Grunt][grunt] tasks included:

    grunt

This will run the default task which uses lessc to preprocess your .less files

    grunt lint

This will lint, using JSHint, your grunt file itself as well as all .js files inside the
js folder.

[nodejs]: http://nodejs.org
[less]: https://github.com/cloudhead/less.js
[volo]: https://github.com/volojs/volo
[grunt]: http://github.com/cowboy/grunt
[sandstone]: http://www.mozilla.org/en-US/styleguide/
