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
### Python 3, Pip, Django, Virtualenv, (virtualenvwrapper optional)
Make sure you are running the latest version of python 3. along with Django.
Links to instruction per OS below

#### Windows
The Django project provides great docs for this. Please follow the instructions to
download python, pip, django and virtualenv. They recommend that you know windows
command prompt, I'd suggest looking at cygwin, or a linux subsystem (windows 10 only)

Windows setup via Django Docs | https://docs.djangoproject.com/en/2.0/howto/windows

setting up cygwin | https://cygwin.com/install.html

windows 10 linux subsystem | https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10

#### Unix Like Systems (Linux, Mac OSX)
if you're running Mac OSX, or linux, most likely python is already installed, but you
may have to upgrade to python 3 (I recommend brew for Mac OSX. apt-get/yum for linux).

You will most likely still need pip (the package manager for python)

installing pip | https://pip.pypa.io/en/stable/installing

pip can then be used to install django

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
to set it up, make sure you are in the directory for the project and run the following:

```sh
virtualenv env
```
this will run a script that creates an python environment you can 'switch into' when you download packages using pip. to switch into it run

```sh
source env/bin/activate
```
this should change the appearance of your prompt. Now, when you use pip, all packages will be downloaded for this virtual environment (because it has its own local copy of pip)

To prevent each members virtual environment from being added to the remote repository a directory called 'env' has been added to the .gitignore file. This prevents it from being pushed up to the github repo. to exit the virtual environment use:

```sh
deactivate
```

## Install Project Python Dependencies With Pip 
a file in the root of the project directory called 'requirements.txt' has been made by pip. to use it, make sure your in your virtualenv 'using the activate script' and run this.

```sh
pip install -r requirements.txt
```

if you install a new dependency and recognize other people will have to use it, you can run
```sh
pip freeze > requirements.txt
```

which will put your installed dependencies in the file. this file is tracked by git, so other members can get the python libraries they will need.

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
