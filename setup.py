#!/usr/bin/env python3

from setuptools import setup

setup(
    name='Aint No Wiki',
    version='3.0.0',
    description='Some sort of a CMS or Wiki',
    author='Andreas Pritschet',
    author_email='andreas@pritschet.me',
    url='https://pritschet.me',
    packages=['aintnowiki',],
    zip_safe=False,
    install_requires=[
        "django=>2.0,<2.1", "django-tinymce", "django-tagging", "django-bootstrap4", "pillow"
    ]
)