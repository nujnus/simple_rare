#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: nujnus
# Mail: 50191646@qq.com
#############################################
  
from setuptools import setup, find_packages

setup(
    name = "simple_rare",
    version = "0.1",
    keywords = ("pip", "simple_rare"),
    description = "generate random data in accordance with relationship of models",
    long_description = "generate random data in accordance with relationship of models",
    license = "MIT Licence",

    url = "",
    author = "nujnus",
    author_email = "50191646@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [],
    scripts = []
)
