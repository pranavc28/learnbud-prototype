"""
Learning app python package configuration.
"""

from setuptools import setup

setup(
    name='learning',
    version='0.1.0',
    packages=['learning'],
    include_package_data=True,
    install_requires=[
        'Flask',
    ],
    python_requires='>=3.6',
)
