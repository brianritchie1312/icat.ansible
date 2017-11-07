ICAT Installer
=========

Installer for ICAT, Topcat and all their dependencies.
Intended for testing purposes.

https://github.com/icatproject
https://icatproject.org/

Requirements
------------

RedHat or Debian OS
Ideally fresh machine but should work regardless
Patience

Role Variables
--------------

See config.yml and .yml files in 'defaults/'

How to use
----------

##### TODO! Improve this tutorial

Install ansible with Yum or Apt

	sudo yum install ansible


	sudo apt install ansible 

Download or clone this repository

Ensure contents are in '/etc/ansible/roles/ICATInstall/'

Create Master Playbook or copy 'exampleplaybook.yml'
	

    - hosts: servers       
      roles:
         - { role: username.rolename, x: 42 }

    - hosts: localhost #Space separated list of hosts. MUST be added to '/etc/ansible/hosts'
      roles:
         - { role: ICATInstall, become: yes, become_user: root }
	

Modify config.yml and yml files in 'defaults/' as desired

Run

	ansible-playbook {MASTER PLAYBOOK NAME}

If running on remote host, add hostname to '/etc/ansible/hosts' and run add the following options

 	ansible-playbook {MASTER PLAYBOOK NAME} --user {SUDO USER ON REMOTE HOST} --ask-pass

If remote hosts include debian systems run

	ansible-playbook {MASTER PLAYBOOK NAME} --user {SUDO USER ON REMOTE HOST} --ask-pass --ask-sudo-pass

##### Notes
* You may need to get valid ssh key before running.
* You can add '-vvvv' to the end of the ansible-playbook command to see better debugging
* You can use '--tags "tag"' or '--skip-tags "tag"' to control which tasks run



Author Information
------------------

Jack Haydock, Computing Apprentice, Science and Technology Facilities Council


Notes
-----

* The setup excutable for the storage plugin returns a fatal error but still performs it's function (currently it's set to ignore this error but this needs to be improved)
* Currently the mysql root password is automatically reset to default before running mysqld_secure_installation, it ignores errors. So having the password set to any other than the variable mysql_root_pass will return an error but will be skipped (including the default password). THIS NEEDS TO BE REPLACED!
* ICATInstall/ must go into '/etc/ansible/roles/'. ICATInstall.yml can go anywhere
* Currently only Simple Authentication is properly implemented
* hosts must be added to /etc/ansible/hosts and have valid ssh keys


TODO
----

* Improve commenting and documentation
* Improve feedback (eg. run automatic tests and report back with the debug module)
* fix Storage setup script not working
* better workaround for mysql root pass
* Learn how ldap works
* figure out how to automatically test plugin installs
* use smaller file for icat ingest
* add checks before package installs and scripts
* Consider replacing env_path with shell scripts for sourcing
* Improve Debug feedback
* Auto grab icat root from first entry in enabled authn user lists


Changelog
---------

#### 07/11/17
* Removed old files...again (there's always one that gets away)
* Minor tidying and comment improvements
* Added SQL script for deleting FACILITY and USER_ entities if requsted
* Fixed pycat_zip check to root dir not user
* Mysql packages are now in a list not a single line string
* Fixed DB users import to prevent duplicate users

#### 03/11/17(2)
* added cleanup

#### 03/11/2017
* Split variables into /defaults
* added version variables into default files
* added users and passwords to master playbook
* added configurable user list allowing any number of users above 1 for simple and db
* moved user creation to main.yml
* added boolean for each playbook (tags still apply)
* added all for authn plugins (no fatal errors but still need deeper testing)
* fixed mysql import module for debian...I think

#### 31/10/2017(2)
* Added albility to choose more than one authn plugin (INCOMPLETE)
* Slightly more tidy
* Added DB Authn install (NOT FULLY TESTED)

#### 31/10/2017
* Tidied up tasks
* Moved user home and working directories to variables (only 11 typos were made!)
* Removed ruby.sh and templates folders

#### 30/10/2017
* Removed Ruby lorem
* Removed Python Lorem
* Added Python ICAT lorem
* started adding checks and comments to playbooks

#### 26/10/2017
* replaced ruby install with python-icat (ICOMPLETE)
* added basic feedback tests to ids and icat playbooks

#### 23/10/2017
* Added ignore error to storage setup bug
* split lorem and ruby into separate playbooks
* fixed ruby and rvm install but gem is still non-functional
* completed multiple OS reorganisation

#### 20/10/2017
* Moved all play to Universal, so they should run on both redhat and debian
* added restart domain to each playbook after glassfish

#### 18/10/2017
* migrated to single role
* split playbooks by OS family and task
