### Summary

This contains the ICAT Install in a single role. It should be operational for RedHat and Debian

### Notes
* The Lorem ipsum script doesn't seem to populate the database - EDIT: this appears to be a result of ruby not installing properly
* This does not work, storage setup script is failing and ruby won't install
* Currently the mysql root password is automatically reset to default before running mysqld_secure_installation, it ignores errors. So having the password set to any other than the variable mysql_root_pass will return an error but will be skipped (including the default password). THIS NEEDS TO BE REPLACED!
* ICATInstall/ must go into '/etc/ansible/roles/'. ICATInstall.yml can go anywhere
* Currently only Simple Authentication is included but the foundations of a system to choose one of several plugin is implemented

### TODO
* Improve commenting and documentation
* Split variables and organise by either OS, function(eg. logins, linesinfiles) or task
* Improve feedback (eg. run automatic tests and report back with the debug module)
* fix Lorem Ipsum not poulating - EDIT: fix ruby install
* fix Storage setup script not working

### Changelog

# 20/10/2017
* Moved all play to Universal, so they should run on both redhat and debian
* added restart domain to each playbook after glassfish

# 18/10/2017
* migrated to single role
* split playbooks by OS family and task
