#! -*- coding: utf-8 -*-

# author: forcemain@163.com


import os


from codecs import open
from setuptools import find_packages, setup


curdir = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(curdir, 'README.md'), 'rb', 'utf-8').read()

setup(
    name='namekox-amqp',
    version='0.0.5',
    description='namekox amqp',
    long_description_content_type='text/markdown',
    long_description=readme,
    author='forcemain',
    url='https://forcemain.github.io/',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=["namekox-core>=0.0.1", "kombu>=3.0.37", "amqp>=1.4.9", "anyjson>=0.3.3"],
    zip_safe=True,
    license='Apache License, Version 2.0',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)