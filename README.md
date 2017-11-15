ICAT Installer
=============
[![Build Status](https://travis-ci.org/JHaydock-Pro/ICAT-Ansible.svg?branch=master)](https://travis-ci.org/JHaydock-Pro/ICAT-Ansible)
 
Installer for ICAT, Topcat and all their dependencies.
Intended for testing purposes.

https://github.com/icatproject
https://icatproject.org/
 

Requirements
------------

* RedHat or Debian flavoured OS and root access
* At least python 2.6
* Ansible and it's dependencies (Only needed on host machine)
* Ideally fresh machine but should work regardless
* Probably a bunch of other stuff I forgot
* Patience
  
Role Variables
-------------

See config.yml and .yml files in 'defaults/'

How to use
----------

1.Install ansible with Yum

	sudo yum install ansible
 
Or Apt

	sudo apt install ansible 
 
2.Download or clone this repository

3.Modify `config.yml` and yml files in `defaults/` as desired

4.Add hosts to `tests/inventory` 

5.Navigate to role directory and run:

	ANSIBLE_CONFIG=ansible.cfg ansible-playbook -i tests/inventory tests/test.yml 

If you are running on localhost, you may need to add

	--connection=local

If you are running on remote hosts, add hostname to inventory and run add the following options

        --user {SUDO USER ON REMOTE HOST} --ask-pass

If remote hosts include debian systems add

        --user {SUDO USER ON REMOTE HOST} --ask-pass --ask-sudo-pass

#### Or

If you prefer to use your own playbook, follow steps 1-3 above then

4.Move role to `/etc/ansible/roles/{ROLE NAME}` or add this to your `/etc/ansible/ansible.cfg` file

	[defaults]
	roles_path={PATH TO DIRECTORY CONTAINING ROLE}

5.Add hostnames to `/etc/ansible/hosts' or add them to your own inventory and add this the the command line

	-i {PATH TO INVENTORY}

6.Copy `tests/test.yml` or the following block into your own yml playbook.

    - hosts: localhost # Any hosts or host groups added to inventory or ansible hosts file separated by spaces
      roles:
         - { role: ICAT-Ansible, become: yes, become_user: root}

Then run

	ansible-playbook {YOUR PLAYBOOK NAME}

##### Notes
* You may need to get valid ssh key before running.
* You can add `-vvvv` to the end of the ansible-playbook command to see more feedback for improved debugging
* You can use `--tags "tag"` or `--skip-tags "tag"` to control which tasks run

  
Author Information
------------------

Jack Haydock, Computing Apprentice, Science and Technology Facilities Council


Notes
-----

* The setup excutable for the storage plugin returns a fatal error but still performs it's function (currently it's set to ignore this error but this needs to be improved)
* Currently the mysql root password is automatically reset to default before running mysqld_secure_installation, it ignores errors. So having the password set to any other than the variable mysql_root_pass will return an error but will be skipped (including the default password). THIS NEEDS TO BE REPLACED!
* The Icat Ingest Script is forced to timeout after 60secs and the resulting error is ignored
* Hosts must be added to `/etc/ansible/hosts` or `tests/inventory` and have valid ssh keys
* All package installs (except pexpect) are set to present instead of latest, this greatly improves speed but may cause some problems if you have an old version of a package but with the same name, I have yet to encounter this (except for Pexpect)

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
* Improve Idempotence
* Add Selenium setup for travis runs

Changelog
---------

#### 15/11/17
* Changed package installs from state:latest to state:present
* Modified README 

#### 12/11/17
* Added Travis
* Moved Inventory and Master YAML (test.yml) inside role
* Added ansible.cfg to allow role to execute from anywhere
* Added world readable tmp files for travis only
* Merged Bash and Sql deletion scripts
* Changed mysql version to 5.6 for debian for Travis
* Tested Authn Plugins with Travis

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
