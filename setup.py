from setuptools import setup

VERSION = "0.0.2"
DESCRIPTION = "Convert enums and structs in a c header to a python equivalent."

setup(
    name='head_to_py',
    version=VERSION,
    description=DESCRIPTION,
    long_description='',
    url='https://www.inverseaudio.co.nz',
    author='Zachary Rogers',
    author_email='z.m.rogers@gmail.com',
    packages=["head_to_py"],
    classifiers=['Development Status :: 1 - Planning'],
)