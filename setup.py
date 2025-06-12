#!/usr/bin/env python3

from setuptools import setup

setup(
    name="lhs",
    version="1.0.0",
    description="Lazy Human Shortcuts - A simple tool to manage zsh aliases permanently",
    author="LHS",
    packages=["lhs"],
    package_dir={"lhs": "python"},
    entry_points={
        'console_scripts': [
            'lhs=lhs.main:main',
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 