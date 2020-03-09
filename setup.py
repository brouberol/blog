#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name='pygments-ext-bash',
    description='Pygments lexer for blog',
    packages=find_packages(),
    install_requires=['pygments >= 1.4'],
    entry_points='''[pygments.lexers]
                    bash=bashlexer:ExtendedBashLexer''',
)

