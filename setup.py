# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='management-agent-it4s',
	version='0.1.1',
	description='Agent to communicate with IT4S management server.',
	url='http://it4s.eu',
	author='IT4S GmbH',
	author_email='support@it4s.eu',
	maintainer='IT4S GmbH',
	maintainer_email='support@it4s.eu',
	license='Commercial',
	packages=find_packages(),
	include_package_data=True,
	zip_safe=False,
	entry_points={
		'console_scripts': [
			'management-agent-it4s = agent:Run'
		]
	}
)
