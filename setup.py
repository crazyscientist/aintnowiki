#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='aintnowiki',
    version='4.0.0',
    description='Some sort of a CMS or Wiki',
    author='Andreas Hasenkopf',
    author_email='andreas@hasenkopf.xyz',
    url='https://hasenkopx.xyz',
    packages=find_packages('aintnowiki'),
    package_dir={"": "aintnowiki"},
    scripts=["aintnowiki/manage.py"],
    zip_safe=False,
    include_package_data=True,
    install_requires=["django>=3.2,<3.3", "djangorestframework", "django-environ"]
)