#!/usr/bin/env python
#

from setuptools import setup

try:
    import numpy as np
except ImportError :
    raise ImportError("Numpy must be installed.")

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

#files_erun = ["energy/energyrun"]

setup(
    name = "convtest_prl",
    version = "1.0.1",
    description = "Convergence test for vasp.",
    author = "Mingqing Liao",
    author_email = "liaomq1900127@163.com",
    url = 'https://github.com/hitliaomq/ConvTest',
    download_url = 'https://github.com/hitliaomq/ConvTest',
    license = "GPL3",
    platforms = ['linux'],
    keywords = ['physics', 'materials', 'convergence test'],
    packages = ['convtest'],
    package_dir = {'convtest': 'src'},
    package_data = {'convtest' : ['kwlist']},
    install_requires = ['numpy'],
    long_description=long_description,
    long_description_content_type='text/markdown',    
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    zip_safe = False
    )