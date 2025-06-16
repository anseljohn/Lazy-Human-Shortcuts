from setuptools import setup, find_packages

setup(
    name="lazy-human-shortcuts",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "lhs=lhs.main:cli",
        ],
    },
    author="John Anselmo",
    description="An AI toolkit manager.",
    url="https://github.com/anseljohn/lazy-human-shortcuts",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 