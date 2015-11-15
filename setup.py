try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from subprocess import Popen, PIPE

from goatd import __version__

setup(
    name='goatd',
    version=__version__,
    author='Louis Taylor',
    author_email='louis@kragniz.eu',
    description=('Experimental daemon to control an autonomous sailing robot'),
    license='LGPL',
    keywords='goat sailing wrapper rest',
    url='https://github.com/goatd/goatd',
    packages=['goatd'],
    scripts=['bin/goatd'],
    requires=['PyYAML'],
    install_requires=[
        'PyYAML >= 3.11'
        ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
