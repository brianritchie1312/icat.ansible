## Summary

Features the steps of the install
WARNING THIS DOES NOT YET WORK ON REMOTE MACHINES ONLY LOCALHOST

## TODO
* Add includes or imports for user accounts
* add variable for mysql_secure reponses
* set up for remote install and test
* set up modular includes/imports for other OSs
* improve commenting on common problems
* encrypt passwords or use vault
* create system to detect when ansible has already been run so that password don't need to be reset
* shut down all processes at end of install (eg. asadmin domains)
* add task to remove files that are no longer needed (eg. zips)
* improve variable organisation (eg. create single config file for whole install)
* Improve modular capabilities
* plan organisation
* fix remote host glassfish domain bug

## Notes
* some Roles are commented out but are needed on clean run
* make sure to run "mysqladmin -u root -p'pw' password ''" after each use of the MySQL Role, I am working on this
* /roles must go in '/etc/ansible/'
* ICATInstall.yml can go anywhere it can be executed

## Changelog

### 16/10/17
* completed Topcat
* Encountered glassfish remote host bug
* INCOMPLETE

### 13/10/17
* completed up to Topcat
* moved downloads to spcific folder for tidyness
* INCOMPLETE

### 12/10/17
* complete ICAT server install
* INCOMPLETE

### 11/10/17
* Completed authn simple
* started Icat server install
* mysql uses default password '' instead of 'pw'
* INCOMPLETE

### 10/10/17
* Completed glassfish install
* started authn simple install
* INCOMPLETE

### 09/10/17
* Initial build
* INCOMPLETE


