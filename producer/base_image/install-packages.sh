#!/bin/bash

# Bash "strict mode", to help catch problems and bugs in the shell
# script. Every bash script you write should include this. See
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ for
# details.
set -euo pipefail

# Tell apt-get we're never going to be able to give manual
# feedback:
export DEBIAN_FRONTEND=noninteractive

# Update the package listing, so we know what package exist:
apt-get update

# Install security updates:
apt-get -y upgrade

# Install a new package, without unnecessary recommended packages:
#apt-get -y install --no-install-recommends syslog-ng # collect logs from machine
apt-get -y install --no-install-recommends apt-utils
apt-get -y install --no-install-recommends libpq-dev
apt-get -y install --no-install-recommends nano
apt-get -y install --no-install-recommends python-scipy
apt-get -y install --no-install-recommends curl
apt-get -y install --no-install-recommends postgresql postgresql-contrib



# Delete cached files we don't need anymore:
apt-get clean
rm -rf /var/lib/apt/lists/*

apt-get autoclean
apt-get autoremove
