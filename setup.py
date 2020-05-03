# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="management-agent-it4smart",
    version="0.1.1",
    description="Agent to communicate with IT4smart management server (sherlock).",
    url="https://it4smart.eu",
    author="IT4smart GmbH",
    author_email="support@it4smart.eu",
    maintainer="IT4smart GmbH",
    maintainer_email="support@it4smart.eu",
    license="Commercial",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={"console_scripts": ["management-agent-it4smart = agent.Run:main"]},
)
