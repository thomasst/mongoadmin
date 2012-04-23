Getting started
===============

Make sure you have the following packages installed:

* Django 1.4
* mongo-python-driver

Make a copy the included default project settings:

    cp mongoadmin_project/settings.py.dist mongoadmin_project/settings.py

Create a database for Django (by default, it is a MySQL database called `mongoadmin`, but you can change it in `DATABASES` in the settings). This database is required to store sessions or to save database connection details.

Fill in `SECRET_KEY` (can be any random string) in the settings.py file that you created.

Run the server:

    python manage.py runserver

Go to http://127.0.0.1:8000/ and connect to your Mongo database.

License
=======
[BSD](http://www.opensource.org/licenses/bsd-license.php)

Ideas for further development
=============================

* Connecting: Store favorites, support for SSH tunnels
* Collection view: Ability to store filters / views
* Support for indexes, etc.
