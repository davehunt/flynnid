from setuptools import setup

setup(
    name = 'FlynnID',
    version = '0.2',
    description='Registers Selenium nodes to a Selenium Grid hub.',
    author = 'Dave Hunt',
    author_email = 'dhunt@mozilla.com',
    url = 'https://github.com/davehunt/flynnid',
    packages = ['flynnid'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        'Programming Language :: Python',
    ],
    entry_points={
        'console_scripts':
            ['flynnid = flynnid:main']
    }
)
