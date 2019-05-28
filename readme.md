
An example application to work with polygons in geojson data
===================================

Works on Python 3.7 with Django 2.2/ Django REST Framework 3.
Fast search querying geodata provided by PostgreSQL 11 with PostGIS
Test service using PostMan, here is <a href="https://documenter.getpostman.com/view/5037826/S1TSYeXJ" target="_blank">sample documentation</a>

About
-----

Allows to create, update, delete, and get polygons
and take a lat/lng pair as arguments and return a list of all polygons that include the given lat/lng

See ``requirements.txt`` for installed packages and the used versions. 

Example guide based on Ubuntu 18.04 installation

Usage
-----



### Install PostgreSQL with PostGIS

    
    sudo apt install binutils
    echo "deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
    sudo nano  /etc/apt/sources.list.d/pgdg.list
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    sudo apt-get update
    
    sudo apt-get install postgresql-11 postgresql-server-dev-11 postgis
    
    sudo -u postgres psql postgres
    
    create user --superuser geodjango  with password 'geopassword';
    
    alter role geodjango set client_encoding to 'utf8';
    
    alter role geodjango set default_transaction_isolation to 'read committed';
    
    create database geodjango owner geodjango;
    alter user geodjango createdb;
    
    CREATE EXTENSION postgis;


### Getting source from the git

Install the required ``requirements.txt`` in the global Python 3 
environment or in a virtual Python 3 environment. The latter has the advantage that 
the packages are isolated from other projects and also from the system wide 
installed global once. If things get messed up, the virtual environment can 
just be deleted and created from scratch again. For more informations about 
virtual environments in Python 3, see venv1_ and venv2_ .

    cd ~
    mkdir geojson-app
    cd geojson-app
    git clone https://github.com/A-Iskakov/django-geojson-app
    sudo pip3 install -r requirements.txt
    python3 manage.py runserver 0.0.0.0:8000


