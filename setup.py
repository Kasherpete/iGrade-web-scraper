from setuptools import setup, find_packages

# Package metadata
NAME = 'igrade'
VERSION = '2.5.2'
DESCRIPTION = 'An unofficial wrapper for iGradePlus Student Management Systems.'
URL = 'https://github.com/Kasherpete/Igrade-web-scraper'
AUTHOR = 'Keagan Peterson'
AUTHOR_EMAIL = 'Keagan.a.peterson@outlook.com'
LICENSE = 'MIT'
LICENSE_URL = 'https://opensource.org/licenses/MIT'

# Package dependencies
INSTALL_REQUIRES = [
    'aiohttp>=2.1.4',
    'requests>=2.1.1',
    'beautifulsoup4>=3.12.2',
    'colorama>=0.2.0',
    'lxml>=3.0.0',
]

# Additional classifiers
CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent'
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
