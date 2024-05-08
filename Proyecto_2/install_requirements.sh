#!/bin/bash

# Check if running as root
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi


# Install python
dnf install -y python3 python3-pip

# Install requirements
pip3 install -r requirements.txt