Databse Dump with ssh and sudo access
=====================================

Database Dump
-------------
To dump the contents of the database, run the following commands:

```
$ sudo su
$ /www/conf_site/manage.sh dumpdata > /www/conf_site/source/conf_site/database_dumps/dump<date>.json
```

Commit this dump to the repository.

Database Load
-------------

In your python directory:

```
$ python manage.py loaddata conf_site/database_dumps/dump<date>.json
```
