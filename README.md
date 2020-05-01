# Management Agent
[![CircleCI](https://circleci.com/gh/IT4smart/ManagementCenter-Agent.svg?style=svg)](https://circleci.com/gh/IT4smart/ManagementCenter-Agent)

The agent is writing in python and it is responsible for the communication with the management console.


## Build dependencies
* dh-systemd
* python-virtualenv
* dh-virtualenv
* python2.7-dev
* python2.7


## Release
The versioning of the management agent follows the "Semantic Versioning" (http://semver.org/).

To create a Release, the version number in the field 'Version' in the file 'setup.py' will be raised. As a result, a 'Commit' will be created with the text 'bump to <Version>'.
This 'Commit' is then to be pushed. After that, the hash of the 'Commits' must be found, then we will hang a tag on this 'Commit'.

To tag it all, we use the following command ``git tag <version> <commit hash>``. Finally, we push this with the command` `git push origin <version>``.


## Packege building
From the sources, a chroot can help building a packet for any architecture. To do that, the GIT-Repository 'BuildSystemRPi' must be downloaded. 
That has to be changed here in the folder 'packages/management-agent'.

Then, enter the following command in the terminal ``make <architecture>``. Currently, the following architectures are supported:
* ARMHF (ARM HardFloat)
* AMD64 (64-bit Architecture, not ARM 64-bit)
* i686 (32-bit Architecture)

When the chroot � environment was successfully loaded, the following command must be entered in the terminal ``export DH_VIRTUALENV_INSTALL_ROOT=/opt/IT4S``.

Afterwards, changes will occur in the directory '/tmp�. The virtual environment for Python must be activated. To do that, we use the command ``source virt-example/bin/activate``.

Now, we change the location of the sources in the directory. The directory is named 'Managementconsole-Agent'. First of all, we change to the "commit" of the most recent tags ``git checkout $(git describe --tags `git rev-list --tags --max-count=1`)``.

Subsenquently, the current Changelog will be always generated with the command ``./changelog > debian/changelog``. 
After that, the command ``dpkg-buildpackage -us -uc`` is to be entered and executed by the Debian packet to create.

## DEV
You can run python linter locally with `sudo docker run --rm -v /opt/it4smart/ManagementCenter-Agent/:/data alpine/flake8 flake8 /data/agent/`