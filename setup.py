#!/usr/bin/env python3

from setuptools import setup

setup(
    name='Aint No Wiki',
    version='3.0.0',
    description='Some sort of a CMS or Wiki',
    author='Andreas Hasenkopf',
    author_email='andreas@hasenkopf.xyz',
    url='https://hasenkopx.xyz',
    packages=['aintnowiki',],
    zip_safe=False,
    install_requires=[
        "django=>2.0,<2.1", "django-tinymce", "django-tagging",
        "django-bootstrap4", "pillow", "django-filebrowser-no-grappelli",
        "sorl-thumbnail"
    ]
)