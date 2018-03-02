<pre>
______ _____  ___ _________  ___ _____ 
| ___ \  ___|/ _ \|  _  \  \/  ||  ___|
| |_/ / |__ / /_\ \ | | | .  . || |__  
|    /|  __||  _  | | | | |\/| ||  __| 
| |\ \| |___| | | | |/ /| |  | || |___ 
\_| \_\____/\_| |_/___/ \_|  |_/\____/ 

        .          |"|         |               ___      
    ,-_-|         _|_|_        |.===.         .|||.     
   ([o o])        (o o)        {}o o{}        (o o)     
ooO--(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo-

</pre>

# SETUP

## Environment Setup
### Python 3, Pip, Flask, Virtualenv, (virtualenvwrapper optional)
Make sure you are running the latest version of python 3. along with Flask.
Links to instruction per OS below

#### Windows
I'd suggest looking at cygwin or winbash, or a linux subsystem (windows 10 only). With that installed
go download pip. with pip, you can install Flask

installing pip | https://pip.pypa.io/en/stable/installing

installing Flask | http://flask.pocoo.org/ 

setting up cygwin | https://cygwin.com/install.html

windows 10 linux subsystem | https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10

#### Unix Like Systems (Linux, Mac OSX)
if you're running Mac OSX, or linux, most likely python is already installed, but you
may have to upgrade to python 3 (I recommend brew for Mac OSX. apt-get/yum for linux).

You will most likely still need pip (the package manager for python)

installing pip | https://pip.pypa.io/en/stable/installing

pip can then be used to install Flask 

### Git
version control will be performed with git. Make sure you either have git, or a git client (tortoisegit or something) using windows. If you have only heard of git, here's a link on getting started.

git docs | https://git-scm.com/book/en/v1/Getting-Started

other useful howto | https://www.taniarascia.com/getting-started-with-git

#### Using git for this project
even if you know git, *read this* . once your repo is cloned, be sure to follow these rules (to prevent screw ups and make life simple)
* pull from the remote repository periodically. do this with 'git pull --rebase'. If you're using a windows client look for a button that looks like it does that.
* I'd recommend making a local branch called dev with 'git branch dev'. you can use 'git checkout [branch name]' to switch branches. this makes it simpler to pull remote changes into your master branch, then merge those with your 'dev' branch.

## Using Virtualenv 
the application environment will run using virtualenv (a python library) which allows each person to use the app on their computer without running into dependency issues. virtualenv makes a local directory storing all dependencies and required versions of python. make sure you have virtualenv installed using pip.

#### Setting up a virtual environment for this project
to set it up, make sure you are inside the directory for the project and run the following:

```sh
virtualenv -p python3 env 
```
this will run a script that creates an python environment you can 'switch into' when you download packages using pip. to switch into it run

```sh
source bin/activate
```
this should change the appearance of your prompt. Now, when you use pip, all packages will be downloaded for this virtual environment (because it has its own local copy of pip)

To prevent each members virtual environment from being added to the remote repository a directory called 'env' has been added to the .gitignore file. This prevents it from being pushed up to the github repo. to exit the virtual environment use:

```sh
deactivate
```

## Install Project Python Dependencies With Pip 
a file in the root of the project directory called 'requirements.txt' has been made by pip. to use it, make sure your in your virtualenv 'using the activate script' and run this.

```sh
pip3 install -r requirements.txt
```

if you install a new dependency and recognize other people will have to use it, you can run
```sh
pip3 freeze > requirements.txt
```

which will put your installed dependencies in the file. this file is tracked by git, so other members can get the python libraries they will need.

## Project Structure
The structure of the app is as follows. This very helpful tutorial on writing a scalable app in Flask by Digitalocean as a starting point and reference.
tutorial | https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications
<pre>
cop4331c_group15_project <-- root directory
+--_run.py <-- entry point, imports app
+--_config.py
+--_app 
   +--_ __init__.py <-- allows run.py to import app as module 
   +--_ auth <-- app.auth 
      +--_ controller.py <-- each modules controller file handles routes
      +--_ models.py     <-- each models file defines the DB schema
      +--_ forms.py      <-- defines the forms using wtforms 
   +--_ user <-- app.user
      +--_ controller.py 
      +--_ models.py 
      +--_ forms.py 
   +--_ listing <-- app.listing
      +--_ controller.py 
      +--_ models.py 
      +--_ forms.py 
   +--_ templates 
      +--_auth
      +--_user
      +--_listing
      +--_admin
      +--_layouts <-- parent templates
         +--_regions   <-- regions of the page (header, footer, head)
         +--_page.html <-- main page template
      +--_macros.jinja <-- jinja macros file to simplify templating
   +--_ static <- static resources (JS, images, css files)
      +--_img
         +--_icons <-- icons for UI
         +--_user  <-- user images
            +--_[1..n] <-- directories named by user.id
         +--_listing   <-- listing images
            +--_[1..n] <-- directories named by listing.id
      +--_js
         +--_src <-- source files
         +--_dist <-- minified, uglified scripts
         +--_lib  <-- third party libraries
      +--_style
         +--_less <-- less files (a CSS preprocessed language)
         +--_css  <-- minified less files
            +--_lib <-- third party CSS files
      +--_gulpfile.js  <-- gulp file used for gulp, see gulp section
      +--_package.json <-- manages dependencies for the gulp build tool 
+--_README.md 
+--_TODO.md 
+--_env 
   +--_<all the virtualenv stuff that you create with "virtualenv -p python3 env"
</pre>

## Running the App
with all of the dependencies installed using pip3, you can run the application with this command at the project root
```sh
python run.py
```
this will start the application on port 8000. to see the result, open a browser and visit http://localhost:8000

## Working On Javascript and CSS
Discussion amonst front end people revealed that we'd be okay using a task runner, which gulp was selected. gulp will watch our .less files and our .js files and will minify it into browser efficient code. To use gulp, first have nodejs and npm installed on your computer (with a terminal). Then, run the following:
```sh
cd cop4331c_group15_project/app/static
# npm will read the package.json file and install everything
npm install
gulp
# you may need to run this too if gulp doesn't work
npm install gulp -g
```
You should see gulp running, which will allow you to change .less files and have the result atomatically minify to css. PLEASE NOTE: you will want to stop gulp before attempting to switch git branches, or performing any commits. Git will usually think that the file has changed if it is re-compiled

## MySQL
All you will need is a MySQL server running on your machine with the following configurations

### Setup
There are a couple of ways to get MySQL running, but if you are a novice, you can use XAMPP which comes bundled with it (and phpmyadmin). otherwise, there's nothing wrong with just running mysql as a unix service using the service command. 

Windows Setup Using XAMPP | http://webdevzoom.com/install-mysql-service-on-windows-using-xampp

Other ways to install it | https://dev.mysql.com/doc/refman/5.7/en/installing.html

if you get a bunch of errors when trying to install python packages using pip regarding mysqlclient please let me know. I had trouble (Mac OSX using homebrew) and had to edit a script called mysql_config.

here's an amusing thread that helped | https://github.com/PyMySQL/mysqlclient-python/issues/169

### Configuration
Make sure you have MySQL running with these settings (most are default) with a database as specified.
* host = localhost
* port = 3306 
* database = group_15_project 
* user = root
* password = ""

### Making Changes to models.py
If you are working on a resource, you may notice a "models.py" file where the schema is defined for that resources table. It is worth noting that SQLAlchemy (the DB abstraction library being used) will not ALTER TABLE for you automatically. In other words, once you run the app, the tables will be created; if you make a change to the model, the tables will need to be dropped in order for SQLAlchemy to make your changes

