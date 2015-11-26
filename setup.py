from setuptools import setup

setup(
    name='pneumatic',
    version='0.0.1',
    description='A bulk upload library for DocumentCloud.',
    url='http://github.com/anthonydb/pneumatic',
    author='Anthony DeBarros',
    author_email='adebarros@gmail.com',
    license='MIT',
    packages=['pneumatic'],
    install_requires=[
        'requests',
    ],
    zip_safe=False
)
