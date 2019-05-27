sudo apt install postgis
sudo apt install binutils

sudo nano  /etc/apt/sources.list.d/pgdg.list

----->
deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main
<<----


wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

sudo apt-get update

sudo apt-get install postgresql-10 postgresql-server-dev-10

sudo -u postgres psql postgres

create user --superuser mploy  with password 'password';

alter role mploy set client_encoding to 'utf8';

alter role mploy set default_transaction_isolation to 'read committed';

alter role mploy set timezone to 'Asia/Almaty';

create database mploy owner mploy;
alter user mploy createdb;


$ createdb  <db name>
$ psql <db name>
> CREATE EXTENSION postgis;