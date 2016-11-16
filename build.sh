#!/bin/bash

# create a virtual environment
virtualenv virt-example

# active virtual environment
source ~/virt-example/bin/active

pip install -U pip
pip install -U setuptools

# package all files
dpkg-buildpackage -us -uc
