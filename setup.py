#!/usr/bin/env python

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='pneumatic',
    version='0.1.8',
    description='A bulk upload library for DocumentCloud.',
    long_description=readme(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    url='http://pneumatic.readthedocs.io/en/latest/',
    author='Anthony DeBarros',
    author_email='practicalsqlbook@gmail.com',
    license='MIT',
    packages=['pneumatic'],
    install_requires=[
        'requests',
        'colorama'
    ],
    exclude_package_data={'': ['.DS_Store']},
    zip_safe=False
)
