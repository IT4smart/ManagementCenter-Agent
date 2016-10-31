#!/bin/bash

# create all debian relevant files
make-deb

chmod +x debian/rules

# package all files
dpkg-buildpackage -us -uc
