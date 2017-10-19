### Summary

This contains the ICAT Install in a single role. Currently it's operational for RedHat OSs.

### Notes
* The Lorem ipsum script doesn't sem to poulate the database
* This only works on RedHat systems
* Currently the mysql root password is automatically reset to default before running mysqld_secure_installation, it ignores errors. So having the password set to any other than the variable mysql_root_pass will return an error but will be skipped (including the default password). THIS NEEDS TO BE REPLACED!
* This install currently takes >16min to install from the start
* ICATInstall/ must go into '/etc/ansible/roles/'. ICATInstall.yml can go anywhere
* Currently only Simple Authentication is included but the foundations of a system to choose one of several plugin is implemented

### TODO
* Check what does and doesn't need separate files or tasks for other OSs and account for it
* Improve commenting and documentation
* Split variables and organise by either OS, function(eg. logins, linesinfiles) or task
* Improve feedback (eg. run automatic tests and report back with the debug module)
* fix Lorem Ipsum not poulating


### Changelog

# 18/10/2017
* migrated to single role
* split playbooks by OS family and task
