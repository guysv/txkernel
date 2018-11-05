# txkernel
# Copyright (C) 2018  guysv

# This file is part of txkernel which is released under GPLv2.
# See file LICENSE or go to https://www.gnu.org/licenses/gpl-2.0.txt
# for full license details.
import os.path
from setuptools import setup, find_packages

here = os.path.dirname(__file__)

with open(os.path.join(here, "README.md")) as readme_file:
    long_description = readme_file.read()

setup(
    name='txkernel',
    version='0.1.0',
    description="Twisted based Jupyter kernel framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guysv/txkernel",
    author="Guy Sviry",
    author_email="sviryguy@gmail.com",
    license="GPLv2",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Interpreters',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='twisted async interactive console jupyter kernel',
    packages=find_packages(),

    install_requires=['twisted', 'txzmq', 'jupyter_core']
)