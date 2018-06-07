ICAT Ansible
============
[![Build Status](https://travis-ci.org/icatproject-contrib/icat.ansible.svg?branch=master)](https://travis-ci.org/icatproject-contrib/icat.ansible)
 
Installer for ICAT, Topcat and all their dependencies.
Intended for testing purposes.

https://github.com/icatproject

https://icatproject.org/
 


Dependencies
------------

* One Master machine with:
	* Yum/Apt enabled OS (eg. Ubuntu).
	* [Ansible](http://docs.ansible.com/ansible/latest/intro_installation.html) and it's dependencies (most are installed automatically with ansible).
		* For Python 2.6/2.7, Ansible version must be at least 2.3 series (2.3.3 tested)
		* For Python 3.5/3.6, Ansible version must be at least 2.5.1 (first version to support Python 3)
	* SSH and root access to all slave machines or 'hosts'.
	* Python 2.6, 2.7, 3.5 or 3.6
		* Python 3.5 is the minimum version of Python 3 supported by Ansible. Note: if you use Python 3, Ansible will run in Python 3 but the python-based ICAT installation scripts will still use Python 2 until they are ported to Python 3.
		* (Selenium Tests will require python >= 2.7 but don't need to run on same machine, see [Topcat_Selenium](https://github.com/JHaydock-Pro/Topcat_Selenium).
* At least one (should support any number) of slave machines to install ICAT on. This can include the master machine, just point it to 'localhost'.
* Patience

  
How to use
----------

1. Install [Ansible](http://docs.ansible.com/ansible/latest/intro_installation.html).

2. Download or clone this repository

3. Modify `config.yml` and yml files in `defaults/` as desired. Or use/create a preset (see below).

4. Add hostnames (of slave machines) to `tests/inventory` 

5. Navigate to role directory and run:

    ```Shell
    ANSIBLE_CONFIG=ansible.cfg ansible-playbook -i tests/inventory tests/test.yml 
    ```

    If localhost is your only slave host, you may need to add

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

If you prefer to use your own playbook to launch the role, follow steps 1-3 above then:

4. Move role to `/etc/ansible/roles/icat.ansible` **or** add this to your `/etc/ansible/ansible.cfg` file

    ```Shell
    [defaults]
    roles_path={PATH TO DIRECTORY CONTAINING ROLE}
    ```

5. Add hostnames to `/etc/ansible/hosts` **or** add them to your own inventory and add this the the command line

    ```Shell
    -i {PATH TO INVENTORY}
    ```

6. Copy `tests/test.yml` **or** the following block into your own yml playbook. (replace 'localhost' chosen slaves in space separated list)

    ```Shell
    - hosts: localhost
      roles:
         - { role: icat.ansible, become: yes, become_user: root}
    ```

7. Then run

    ```Shell
    ansible-playbook {YOUR PLAYBOOK NAME}
    ```

##### Here are some useful options to add onto command line

| Option                              | Function |
|:-----------------------------------:|:--------:|
| -vvvv                               | Add extra verbosity, increase output text (useful for debugging) |
| --list-tags                         | List tags used in role. |
| --tags "tag1, tag2,..."             | Only play tasks tagged with whatever you put in the quotes (use comma separation for multiple tags). |
| --skip-tags "tag1, tag2,..."        | Play all tasks except those in the quotes. Some tasks have the 'always' tag, meaning they will always be run unless `--skip-tags "always"` is used, regardless of how other tags are setup and skipped. |
| --diff                              | Detailed look at what changes have been made to files. |
| -e, --extra-vars "varname=varvalue" | Overwrite variables from the command line , see 'presets' below. Use a space separated list. Note Boolean values don't seem to work in this format. |
| -e '{varname: varvalue}'            | Same as above but boolean values should work in this format. However in this format every variable needs it's own '-e' |

*NOTE: if you need a large number of extra vars, consider using a preset, see below.*

You can find more here: https://www.mankier.com/1/ansible-playbook

If you wish to reduce clutter you can stop skipped tasks from playing by adding `display_skipped_hosts = False` to `ansible.cfg`  
or you can add `stdout_callback = actionable` to ansible.cfg to only display tasks that return changed or failed.


Role Variables
-------------

Most variables are stored in `config.yml` or in .yml files in `/defaults/`. Most variables are separated by plugin, however some plugin variables are used by multiple plugins (eg. container list).


Variables are called with jinja2 templating and ansible supports many jinja [filters](http://docs.ansible.com/ansible/latest/playbooks_filters.html).


Variables can also be stored as [lists or dictionaries](http://docs.ansible.com/ansible/latest/YAMLSyntax.html#yaml-basics). Lists can be used in [loops](http://docs.ansible.com/ansible/latest/playbooks_loops.html).


All variables can be plain text or [hash encrypted](http://docs.ansible.com/ansible/latest/faq.html#how-do-i-generate-crypted-passwords-for-the-user-module). Ansible also supports [hash filters](http://docs.ansible.com/ansible/latest/playbooks_filters.html#hash-filters) and [vaults](http://docs.ansible.com/ansible/latest/playbooks_vault.html). If you are using any actual data/passwords then vaults should be used.




Presets
-------
There are several preset configurations for convenience in the `presets/` directory. These are yml/json files with lists of variables to overwrite allowing for easy reconfiguration without digging around in the config.yml or other variable files.

To use them simply add this to the command line.

```Shell
--extra-vars "@presets/filename.yml"
```

For example, this adding this to the command line will run the installer with variables specialised for travis testing icat.server 4.9.1

```Shell
--extra-vars "@presets/travis_4.9.1.yml"
```


*Note: These will only overwrite the variables that are specified, any variables not in the file will be taken from elsewhere.*


Tested Configurations
---------------------

These configurations have only been tested to a basic level (ie. they run without fatal errors and the end product seems to be operational). These configuration should match the config files in presets/.

| Config       | OSs              | MySQL | Glassfish | Payara   | authn.simple | authn.db | authn.ldap | authn.anon | icat.lucene | icat.server | ids.server | ids.storage_file | topcat |
|:------------:|:----------------:|:-----:|:---------:|:--------:|:------------:|:--------:|:----------:|:----------:|:-----------:|:-----------:|:----------:|:----------------:|:------:|
|Default_4.9.1 | Sl6/Ubuntu 14.04 |5.1.73 |--         |4.1.2.174 |2.0.0         |2.0.0     |--          |--          |1.1.0        |4.9.1        |1.8.0       |1.4.0             |2.3.6   |
|Travis_4.9.1  | Ubuntu 14.04     |5.6    |--         |4.1.2.174 |2.0.0         |2.0.0     |2.0.0       |2.0.0       |1.1.0        |4.9.1        |1.8.0       |1.4.0             |2.3.6   |
|Default_4.8.0 | SL6/Ubuntu 14.04 |5.1.73 |4.0        |--        |1.1.0         |1.2.0     |1.2.0       |1.1.1       |--           |4.8.0        |1.7.0       |1.3.3             |2.2.1   |

Selenium
--------

https://github.com/JHaydock-Pro/Topcat_Selenium

To run the selenium tests (Topcat UI testing), you will need python 2.7.

This test is **NOT** automatically run by ansible, however if 'selenium: true' is set in config.yml or a preset it will setup the environment for the script to be run by travis or a user. The script should be able to be run by ansible but a user won't be able to read it's output.

Example (as user1):
```Shell
cd ~/Topcat_Selenium
python topcat_selenium_test.py --url http://localhost:8080 --user-data simple root pass --user-nodata db root password --virtual-display
```

Notes
-----

* Some tasks will fail even when correct (Mysql password reset and icat ingest). These errors are ignored with a conditional fail following them. It should return a fatal error if the previous task failed in anyway that was not the expected failure (eg. the ingest returns a different error than async timeout).
* Hosts must be added to `/etc/ansible/hosts` or `tests/inventory` and have valid ssh keys, simply SSHing into target machine once beforehand should work.
* Many package installs (except pexpect) are set to present instead of latest, this greatly improves speed but may cause some problems if you have an old version of a package but with the same name, I have yet to encounter this (except for Pexpect). Simply replace `state: present` with `state: latest`.
* If you already have mysql installed be sure to change the `mysql_root_pass` variable in `config.yml`
* If you are using a VM with pip 1.0 installed, run `pip install --index-url=https://pypi.python.org/simple/ -U pip` to upgrade.
* Some tasks involve finding a file with partial name instead of an absolute path. In these cases it will select the first matching file. For example If you have multiple 'mysql-connector-java-*.jar' files in /usr/share/java it will only use the first one. 
* Sometimes adding boolean variables to --extra-vars cause them to return false even when set to true, assigning the value in a preset file seems to work anyway.
* Some older versions of plugins don't seem to have '/{plugin}/version' urls or have different ones, so if running older versions (eg. default_4.8.0) you may need to add `--skip-tags "check"` to the command line
* If you wish to change the installed version of a plugin, you may need to remove the current version (ie. delete the entire directory) as the zipfiles won't extract when the plugin directory already exists
* If are seeing images of cows you have cowsay installed, add `ANSIBLE_NOCOWS=1` to command line or `ansible.cfg`. Alternativly you could use `cowsay -l`, pick one of the options then add `ANSIBLE_COW_SELECTION=<your chosen 'cow'>` to command line or `ansible.cfg` and have some fun. You can install cowsay with `apt/yum install cowsay`.



TODO
----

* Universal
    * Improve commenting and documentation (eg. full tutorials, detailed descriptions of how things are ordered)
    * Learn how ldap works and implement proper setup and test if possible
* Ansible
    * General    
        * Improve Idempotence
    * Workarounds
        * Consider replacing env_path with shell scripts for sourcing
    * topcat.json
        * Create task to remove all disabled facilities from topcat.json
    * Misc
        * Setup Non-LILS facility
        * Split Topcat Admin user into Data/Admin User
        * Make pycat.yml more adaptable (eg. pycat version numbers, control which user gets data, clearer args"
        * Figure out ids.storage url check (ie. /{plugin}/version)
        * Figure out how to test older plugins without url '/version' or figure out the earliest version with them and skip test on earlier versions
* Selenium
    * See [Topcat_Selenium](https://github.com/JHaydock-Pro/Topcat_Selenium)
* Travis
    * Test Idempotence




Changelog
---------

#### 02/02/18
* Temporary removal of chrome from Topcat_Selenium arguments due to latest release bug, see [Topcat_Selenium]{https://github.com/JHaydock-Pro/Topcat_Selenium} for details

#### 24/01/18
* Removed browser installs, now handled by travis or user

#### 23/01/18
* removed ignore_errors from storage setup, it just seems to work consistently now, no idea why
* corrected regexp for replace task in topcat.json

#### 19/01/18
* Selenium now uses get_url instead of downloading the zip
* Removed log and output files

#### 18/01/18
* Improved regexp

#### 16/01/18
* Separated Selenium script (moved to https://github.com/JHaydock-Pro/Topcat_Selenium)

#### 11/01/18
* Renamed yml files for organisation purposes. (The fact that the alphabetical order is slightly different to the order they are run really annoys me)
    * 'main.yml' is unchanged, it's name is important
    * Root installed depencies start with 'dep_'
    * User installed plugins and container start with 'setup_'
    * Testdata and selenium start with 'test_'
    * Tasks included in multiple yml files start with 'include_'
    * 'lucene' is now 'icat_lucene'
    * 'icat' is now 'icat_server'
    * 'ids' is now 'ids_server'
    * 'storage' is now 'ids_storage'
* Renamed high level variables (those in config.yml) to similar pattern from above. Lower level variables are unchanged and considering how tedious it was to change the high level ones, they'll probably stay that way
    * 'lucene' is now 'icat_lucene'
    * 'icat' is now 'icat_server'
    * 'ids' is now 'ids_server'
    * 'storage' is now 'ids_storage'
* Corrected some missing variables
* Added 'check' tag to skip url checks (some older plugins don't seem to have '/version' urls)
* Readded 'your facility...' replaced by fac_short_name in topcat.json, it's only needed in older versions but is safe to leave in for newer versions
* Improved Readme
* Removed old utils.yml

#### 10/01/18(2)
* Minor Output Improvements in selenium script
* selenium.yml installs firefox and chrome if variable set in config.yml
* Removed firefox, chrome, pyvirtual display install from travis

#### 10/01/18
* Improved Commenting
* Disabled authn plugins are now removed from topcat.json, the solution is imperfect but functional

#### 09/01/18
* Improved Commenting
* Download and Uzip tasks moved into separate file 'download.yml'. Condensing four tasks into one with vars
* Download Directory creation moved to download.yml
* preplay.yml renamed to startdomain.yml and removed from container playbook

#### 08/01/18
* topcat.yml now only replaces 'https://' instead of 'https' then replacing transport type back
* Facilty name now stored as two variables 'fac_short_name' and 'fac_long_name' overwrites LILS (Experimental!)
* Ingest dump filename now variable (ingest_file)
* Ids only copies storage*.jar if storage=true
* IDS archive line only commented out if two_level=false
* DB user/pass list now deleted after use
* Slightly Improved commenting 

#### 05/01/18(2)
* Attempted Chrome fix for travis
* Changed variable names for webdrivers to avoid confusion
* Topcat_test directory now a variable
* gecko.sh uses relative path instead of absolute

#### 05/01/18
* Downloaded Zip existence check added to topcat_test
* Removed unused 'Create Download Dir' print function from topcat_test
* Removed 'file existence not checked' warnings from download tests in topcat_test
* Shortened file existence ouput to just basename instead of full path (parent directory printed at begining of output)
* Changed datafile name to variable, not yet configurable from outside script

#### 21/12/17
* Added More tests to selenium
    * Check file downloaded by action exists in folder
    * Check Renaming zip works without error
    * Check https and globus are both selectable options
* Selenium now creates new directory with timestamp as name for downloads (Ensures only downloads from respective run will be present in path)

#### 20/12/17 (2)
* Add conditional fail to mysql password reset. If command fails for any reason other than wrong password it will fail the build. 
* Added some extra tags to pycat.yml to allow skipping ingest or file creation. This means output won't be pushed out of frame by massive ammounts of output from ingest and create file tasks.
* Corrected some nameless tasks in pycat.yml

#### 20/12/17
* Removed with_items from authn.yml includes, this means it will no longer say authn has failed conditional when tag other than authn is used.
* Added curl tests to; authn plugins, lucene, icat.server, ids.server and topcat. Tests for payara, glassfish and ids.storage are needed.

#### 19/12/17
* Added facilty arguments to README
* Attempted to split root user into data/admin (failed: but replaced icat_root with icat_admin)
* Removed old selenium script
* Added conditional to ingest so if it fails for any reason other than timeout it should fail build (experimental)

#### 18/12/17 (2)
* Add facilty arguments to Selenium Script
* Further Improved Output of Selenium Script

#### 18/12/17
* Reorganised Master functions in selenium script
* Further Improved Output of Selenium
* Corrected typo in tasks/topcat.yml
* Corrected example CL in README

#### 15/12/17
* Extra tests in selenium script
* Minor improvements and fixes in selenium script
* Added ANSI colour and formatting to script output, making failures easier to spot
* Added variable for ingest timeout (default = 60s, travis = 120s)
* Temporary removal of chrome from test_args until chrome works

#### 14/12/17
* Major restructure of topcat_test.py (selenium script). It's much longer but is also more organised and easier to read.
* Corrected lucene IP
* Added extra arguments to topcat_test.py
* Split Root and Non-Root users into Data User, No Data User and Admin User in selenium script (TODO do same for ansible)

#### 11/12/17
* Travis now fails if 'Failed' is found in selenium output

#### 11/12/17
* Added selenium setup playbook

#### 05/12/17
* Replaced payara_src

#### 4/12/17
* Fixed Topcat Issue (replace module was replace transport type, 'http' is not a transport type, 'https' is)
* Added install tags to setup scripts

#### 1/12/17
* PolyVersion branch should now work
* Fixed missing icatUrl in topcat.json for topcat 2.3.0 and above
* Added command line configuration files
* Added payara install
* Added names to all tasks, including stat, set_fact and debug tasks
* Added version numbers to play_names
* Improved variable version numbers. Url and Filenames should be automatically changed depending on versions
* Created presets for overwrittig variables from command line

#### 28/11/17
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

