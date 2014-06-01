from distutils.core import setup

import goatd

setup(
    name='goatd',
    version=str(goatd.VERSION) + '.0',
    author='Louis Taylor',
    author_email='kragniz@gmail.com',
    description=('Experimental daemon to control an autonomous sailing robot'),
    license='LGPL',
    keywords='goat sailing wrapper rest',
    url='https://github.com/goatd/goatd',
    packages=['goatd'],
    scripts=['goatd-start'],
    requires=['PyYAML'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
