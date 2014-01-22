try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='mixpanel-py-async',
    version='0.0.1',
    author='Jesse Pollak',
    author_email='jpollak92@gmail.com',
    packages=['mixpanel_async'],
    url='https://github.com/jessepollak/mixpanel-python-async',
    description='Python library for using Mixpanel asynchronously',
    long_description=open('README.md').read(),
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