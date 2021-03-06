#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')

VERSION = get_version('luzfcb_dj_simplelock', '__init__.py')

if sys.argv[-1] == 'publish':
    try:
        import wheel  # NOQA
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (VERSION, VERSION))
    os.system("git push --tags")
    sys.exit()

with open('README.rst') as readme_file:
    readme = readme_file.read()  # NOQA

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')  # NOQA

setup(
    name='luzfcb_dj_simplelock',
    version=VERSION,
    description="""para evitar edição concorrente, concede temporariamente"""
                """a capacidade de edição exclusiva de uma instancia de um model para um determinado usuario""",
    long_description=readme + '\n\n' + history,
    author='Fabio C. Barrionuevo da Luz',
    author_email='bnafta@gmail.com',
    url='https://github.com/luzfcb/luzfcb_dj_simplelock',
    packages=[
        'luzfcb_dj_simplelock',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='luzfcb_dj_simplelock',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
