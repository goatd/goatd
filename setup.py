try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from subprocess import Popen, PIPE

setup(
    name='goatd',
    version='3.0.0',
    author='Louis Taylor',
    author_email='louis@kragniz.eu',
    description=('Experimental daemon to control an autonomous sailing robot'),
    license='LGPL',
    keywords='goat sailing wrapper rest',
    url='https://github.com/goatd/goatd',
    package_dir = {
        'goatd': 'goatd',
        'goatd.coreplugins': 'goatd/coreplugins',
        'goatd.coreplugins.mavlink_common': 'goatd/coreplugins/mavlink_common',
    },
    packages=['goatd', 'goatd.coreplugins', 'goatd.coreplugins.mavlink_common'],
    scripts=['bin/goatd'],
    install_requires=[
        'PyYAML',
        'six',
        'pyserial',
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
