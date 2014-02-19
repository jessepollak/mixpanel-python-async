try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
long_description = 'Python library for using Mixpanel asynchronously. For more info, visit http://github.com/jessepollak/mixpanel-python-async.'
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()

setup(
    name='mixpanel-py-async',
    version='0.0.2',
    author='Jesse Pollak',
    author_email='jpollak92@gmail.com',
    packages=['mixpanel_async'],
    url='https://github.com/jessepollak/mixpanel-python-async',
    description='Python library for using Mixpanel asynchronously',
    long_description=long_description,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    test_suite='tests',
    install_requires=[
        'mixpanel-py'
    ]
)