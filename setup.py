#!/usr/bin/env python

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='pneumatic',
    version='0.1',
    description='A bulk upload library for DocumentCloud.',
    long_description=readme(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    url='http://pneumatic.readthedocs.org/',
    author='Anthony DeBarros',
    author_email='adebarros@gmail.com',
    license='MIT',
    packages=['pneumatic'],
    install_requires=[
        'requests',
    ],
    zip_safe=False
)
