#!/bin/bash -e


BASEDIR=`dirname $0`/..

#echo $BASEDIR

# create a virtual environment
if [ ! -d "$BASEDIR/virt-example" ]; then
    virtualenv -q $BASEDIR/virt-example --no-site-packages
    echo "Virtualenv created."
fi


# active virtual environment
source $HOME/virt-example/bin/active

# check if we are in the virtual environment
INVENV=$(python -c 'import sys; print ("1" if hasattr(sys, "real_prefix") else "0")')

if [ "${INVENV}" = 1 ] ; then
    cd $BASEDIR
    pip install -U pip
    pip install -U setuptools

    # package all files
    #dpkg-buildpackage -us -uc
fi