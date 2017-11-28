# THIS BRANCH IS INCOMPLETE AND WILL NOT WORK!

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
* Ideally a fresh machine but should work regardless
* Probably a bunch of other stuff I forgot
* Patience
  
Role Variables
-------------

See `config.yml` and .yml files in `defaults/`

How to use
----------

1. Install [Ansible](http://docs.ansible.com/ansible/latest/intro_installation.html). The simplest method is.

    ```Shell
    sudo apt-get install python-pip
    pip install ansible
    ```

2. Download or clone this repository

3. Modify `config.yml` and yml files in `defaults/` as desired

4. Add hosts to `tests/inventory` 

5. Navigate to role directory and run:

    ```Shell
    ANSIBLE_CONFIG=ansible.cfg ansible-playbook -i tests/inventory tests/test.yml 
    ```

If you are running on localhost, you may need to add

```Shell
--connection=local
```

If you are running on remote hosts, add hostname to inventory and run add the following options

```Shell
--user {SUDO USER ON REMOTE HOST} --ask-pass
```

If remote hosts include debian systems add

```Shell
--user {SUDO USER ON REMOTE HOST} --ask-pass --ask-sudo-pass
```

## Or

If you prefer to use your own playbook, follow steps 1-3 above then

4. Move role to `/etc/ansible/roles/{ROLE NAME}` or add this to your `/etc/ansible/ansible.cfg` file

    ```Shell
    [defaults]
    roles_path={PATH TO DIRECTORY CONTAINING ROLE}
    ```

5. Add hostnames to `/etc/ansible/hosts' or add them to your own inventory and add this the the command line

    ```Shell
    -i {PATH TO INVENTORY}
    ```


6. Copy `tests/test.yml` or the following block into your own yml playbook.

    ```Shell
    - hosts: localhost # Any hosts or host groups added to inventory or ansible hosts file separated by spaces
      roles:
         - { role: ICAT-Ansible, become: yes, become_user: root}
    ```

7. Then run

    ```Shell
    ansible-playbook {YOUR PLAYBOOK NAME}
    ```

##### Here are some useful options to add onto command line

| Option                        | Function |
|:-----------------------------:|:--------:|
| -vvvv                         | Add extra verbosity, increase output text (useful for debugging) |
| --list-tags                   | List tags used in role. |
| --tags "tag1, tag2,..."       | Only play tasks tagged with whatever you put in the quotes (use comma separation for multiple tags). |
| --skip-tags "tag1, tag2,..."  | Play all tasks except those in the quotes. Some tasks have the 'always' tag, meaning they will always be run unless `--skip-tags "always"` is used, regardless of how other tags are setup and skipped. |
| --diff                        | Detailed look at what changes have been made to files. |

You can find more here: https://www.mankier.com/1/ansible-playbook

If you wish to reduce clutter you can stop skipped tasks from playing by adding `display_skipped_hosts = False` to `ansible.cfg`  
or you can add `stdout_callback = actionable` to ansible.cfg to only display tasks that return changed or failed.

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
* If you already have mysql installed be sure to change the `mysql_root_pass` variable in `config.yml`
* If you are using a VM with pip 1.0 installed, run `pip install --index-url=https://pypi.python.org/simple/ -U pip` to upgrade.
* Some tasks involve finding a file with partial name and no absolute path. In these cases it will select the first matching file. For example If you have multiple 'mysql-connector-java-*.jar' files in /usr/share/java it will only use the first one. 


TODO
----

* Improve commenting and documentation
* Improve feedback (eg. run automatic tests and report back with the debug module)
* Fix Storage setup script not working
* Better workaround for mysql root pass
* Learn how ldap works
* Figure out how to automatically test plugin installs
* Use smaller file for icat ingest
* Consider replacing env_path with shell scripts for sourcing
* Improve Debug feedback
* Auto grab icat root from first entry in enabled authn user lists
* Improve Idempotence and speed
* Add Selenium setup for travis runs
* Add Payara Conditional
* Reconfigure to allow removal of glassfish
* Update with ICAT 4.9.1


Tested Configurations
---------------------

These configurations have only been tested to a basic level (ie. they run without fatal errors and the end product seems to be operational).

| Config     | OS         | Ansible | Java | Python | MySQL | Glassfish | Payara | Simple Authn | DB Authn | LDAP Authn | Anon Authn | ICAT | IDS | IDS Storage | Python-ICAT | Topcat |
|:----------:|:----------:|:-------:|:----:|:------:|:-----:|:---------:|:------:|:------------:|:--------:|:----------:|:----------:|:----:|:---:|:-----------:|:-----------:|:------:|
|RedHat #1   |SL6         |2.3.1.0  |1.8.0 |2.6.6   |5.1.73 |4.0        |--      |1.1.0         |1.2.0     |1.2.0       |1.1.1       |4.8.0 |1.7.0|1.3.3        |0.13.01      |2.2.1   |
|Debian #1   |Ubuntu 14.04|2.3.1.0  |1.8.0 |2.6.6   |5.1.73 |4.0        |--      |1.1.0         |1.2.0     |1.2.0       |1.1.1       |4.8.0 |1.7.0|1.3.3        |0.13.01      |2.2.1   |
|Travis CI   |Ubuntu 14.04|2.4.1.0  |1.8.0 |2.7.13  |5.6    |4.0        |--      |1.1.0         |1.2.0     |1.2.0       |1.1.1       |4.8.0 |1.7.0|1.3.3        |0.13.01      |2.2.1   |


Changelog
---------

#### 28/11/17 INCOMPLETE
* Replaced glassfish with container to include payara
* removed separate glassfish and payara files
* Replaced urls and properties filenames with conditionals depending on version
* Moved version numbers to config.yml
* attempted 4.9.1

#### 27/11/17
* Replaced blockinfiles with lineinfiles and lists. This should, in theory, make version changing easier as any extra lines in new versions of properties files won't be overwritten, new lines will have to be manually configured if default is correct.
* Condensed Authn variables into one set for all four. (ie. One url varable with it's own varaibles for each run of authn.yml rather than four near identical variables)

#### 24/11/17(2)
* mysql service name defaults to 'mysql' if nothing is found in /etc/init.d/
* Added pkg list to be installed before anything else is run, meant to install anything the default OS may miss (eg. unzip, pip )
* If mysql 5.6 is installed package names for apt will be updated to prevent errors

#### 24/11/17
* Conditionals are now decided by pkg_mgr (ie. yum or apt) rather than OS family, this should hopfully allow other OSs to work.
* OS specific files and filepaths are now decided by what ansible can find rather than specific file (eg. It will find and copy the first 'mysql-connector-java-*.jar' file in /usr/share/java rather than a specific version specified for each OS.
* Glassfish script path set to user_home instead of OS specific paths.

#### 23/11/17
* Corrected transport url in topcat.json
* Commented out archive settings in ids.properties

#### 22/11/17
* Added tested configurations to README
* Added Pycat version variable

#### 20/11/17
* Improved Documentation
* Moved main.yml variables (user_home and download_dir) to config.yml
* Minor Idempotence Improvements (Currently 37 changes on second run)
* Added Firefox and Chrome Installs to travis, selenium script not yet added 

#### 16/11/17
* Added File Creation (By name or all)

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
