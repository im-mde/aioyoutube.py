from setuptools import setup, find_packages

AUTHOR = 'im-mde'
VERSION = '0.6.0'
DESCRIPTION = 'An asynchronous Python wrapper for the YouTube Data API'

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

long_description = ''
with open('README.MD') as f:
    long_description = f.read()

setup(
    name='aioyoutube.py',
    author=AUTHOR,
    url='https://github.com/im-mde/aioyoutube.py',
    version=VERSION,
    packages=['aioyoutube'],
    license='MIT',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.7',
    classifiers=[
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Topic :: Internet',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
    ]
)