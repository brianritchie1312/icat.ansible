### Summary

This contains the ICAT Install in a single role. It should be operational for RedHat and Debian. It currently does not work unless you add '--skip-tags "broken"' to the end of the command line, this skips the lorem ipsum test script which is currently not working.

### Notes
* Ansible can't seem to find the 'gem' command and the gem module can't find the faker gem
* The setup excutable for the storage plugin returns a fatal error but still performs it's function (currently it's set to ignore this error but this needs to be improved)
* Currently the mysql root password is automatically reset to default before running mysqld_secure_installation, it ignores errors. So having the password set to any other than the variable mysql_root_pass will return an error but will be skipped (including the default password). THIS NEEDS TO BE REPLACED!
* ICATInstall/ must go into '/etc/ansible/roles/'. ICATInstall.yml can go anywhere
* Currently only Simple Authentication is included but the foundations of a system to choose one of several plugin is implemented

### TODO
* Improve commenting and documentation
* Split variables and organise by either OS, function(eg. logins, linesinfiles) or task
* Improve feedback (eg. run automatic tests and report back with the debug module)
* fix gem install on ruby playbook
* fix Storage setup script not working
* add checking to prevent uneccesary downloading

### Changelog

# 23/10/2017
* Added ignore error to storage setup bug
* split lorem and ruby into separate playbooks
* fixed ruby and rvm install but gem is still non-functional
* completed multiple OS reorganisation

# 20/10/2017
* Moved all play to Universal, so they should run on both redhat and debian
* added restart domain to each playbook after glassfish

# 18/10/2017
* migrated to single role
* split playbooks by OS family and task
