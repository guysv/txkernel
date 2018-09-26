# txkernel
# Copyright (C) 2018  guysv

# This file is part of txkernel which is released under GPLv3.
# See file LICENSE or go to https://www.gnu.org/licenses/gpl-3.0.txt
# for full license details.

from setuptools import setup, find_packages

setup(
    name='txkernel',
    version='0.1.0',
    packages=find_packages(),

    install_requires=['twisted', 'txzmq', 'jupyter_core']
)