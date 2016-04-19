"""
Sample project to be edited.
"""
from pip.req import parse_requirements
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand
import sys
import os


# Workaround for development under Vagrant using vbox shared directories
# Hard links aren't allowed which breaks setup.
# Is a quick hack that fixes the issue just under vagrant with vbox
# From stackoverflow:
# https://stackoverflow.com/questions/7719380/python-setup-py-sdist-error-operation-not-permitted
# if you are not using vagrant, just delete os.link directly,
# The hard link only saves a little disk space, so you should not care
if os.environ.get('USER','') == 'vagrant':
    del os.link

class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)



dependencies = ['click==4.1', 'rdflib', 'rdflib-jsonld',
                'orcid', 'orcidfind', 'pyparsing', 'pytz', 'requests==2.7.0', 'docker-py']

setup(
    name='smartcontainers',
    version='0.0.2',
    url='https://github.com/charlesvardeman/smartcontainers',
    license='Apache Software License',
    author='Charles Vardeman',
    author_email='charles.vardeman@gmail.com',
    description='Tool to track provenance of docker containers',
    long_description=__doc__,
    packages=find_packages(exclude=['tests', 'docs', 'scripts', 'resources']),
    include_package_data=True,
    dependency_links=[
        "git+ssh://git@github.com/charlesvardeman/orcidfind/tarball/master#egg=orcidfind"
    ],
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    tests_require=['tox'],
    cmdclass = {'test': Tox},
    entry_points={
        'console_scripts': [
            'sc= sc.cli:cli',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
