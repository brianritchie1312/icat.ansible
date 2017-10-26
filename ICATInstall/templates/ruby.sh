#! /bin/bash

echo "Downloading rvm"
curl -sSL {{ rvm_url }} | bash

echo "Sourcing rvm"
source ~/.rvm/scripts/rvm

echo "installing 2.4.2"
rvm install 2.4.2 --default

echo "checking ruby version"
rvm current
ruby --version
which ruby
which gem

export PATH="/home/{{ user_name }}/.gem/ruby/2.4.0/bin:$PATH"

echo "installing gems"
gem install faker --user-install
#gem install rest-client

echo "running script"
ruby test_data_generator.rb
