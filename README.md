## Summary

Features the steps of the install up to end of Icat server

## TODO
* Complete other roles, see ICATInstall.yml
* Add includes or imports for user accounts
* add variable for mysql_secure reponses
* set up for remote install and test
* set up modular includes/imports for other OSs
* improve commenting on common problems
* encrypt passwords
* create system to detect when ansible has already been run so that password don't need to be reset
* shut down all processes at end of install (eg. asadmin domains)

## Notes
* some Roles are commented out but are needed on clean run
* make sure to run "mysqladmin -u root -p'pw' password ''" after each use of the MySQL Role, I am working on this
* /roles must go in '/etc/ansible/'
* ICATInstall.yml can go anywhere it can be executed

## Changelog

### 0.1.3
* complete ICAT server install
* INCOMPLETE

### 0.1.2
* Completed authn simple
* started Icat server install
* mysql uses default password '' instead of 'pw'
* INCOMPLETE

### 0.1.1
* Completed glassfish install
* started authn simple install
* INCOMPLETE

### 0.1.0
* Initial build
* INCOMPLETE


