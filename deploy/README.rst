Deployment Files
================

This directory contains files that are used for deployment.
The fab file we use will look in this directory for templates,
configuration files, and files that are optional and not
checked in to the repo, such as secrets.

Files that will not be checked in
---------------------------------

* secrets.py: this file should contain secrets that get used 
  in production and staging sites.
* authorized_keys: this is an optional file that should not be
  checked in. It can contain public ssh keys for people who are
  administrators.
