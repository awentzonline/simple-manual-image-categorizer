#!/usr/bin/env python
from distutils.core import setup


setup(
    name='simple-manual-image-categorizer',
    version='0.0.1',
    description='A simple manual image categorizer',
    author='Adam Wentz',
    author_email='adam@adamwentz.com',
    url='https://github.com/awentzonline/smic',
    packages=[
        'smic',
    ],
    install_requires=[
        'Pillow',
    ],
    entry_points={
        'gui_scripts': [
            'smic = smic.__main__:main',
        ]
    }
)
