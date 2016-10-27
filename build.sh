#!/bin/bash

# create all debian relevant files
make-deb

# package all files
dpkg-buildpackage -us -uc
