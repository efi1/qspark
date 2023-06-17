"""Minimal setup file for Kazuar assignment."""

from setuptools import find_packages
from distutils.core import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='request locates',
    version='0.1.0',
    description='Q-Spark Assignment',
    packages=find_packages('src'),
    package_dir={'': 'src'},

    # metadata
    author='Efi Ovadia',
    author_email='efovadia@gmail.com',
    license='proprietary',
    install_requires = [required, 'pytest']
)