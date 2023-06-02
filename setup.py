from setuptools import setup, find_packages

# Package metadata
NAME = 'igrade'
VERSION = '2.5.0'
DESCRIPTION = 'An unofficial wrapper for iGradePlus Student Management Systems'
URL = 'https://github.com/Kasherpete/Igrade-web-scraper'
AUTHOR = 'Keagan Peterson'
AUTHOR_EMAIL = 'Keagan.a.peterson@outlook.com'
LICENSE = ''

# Package dependencies
INSTALL_REQUIRES = [
    'aiohttp~=3.8.4',
    'requests~=2.25.1',
    'beautifulsoup4~=4.12.2',
    'colorama~=0.4.6',
    'lxml~=4.9.0',
]

# Additional classifiers
CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
]

# Package setup
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
)
