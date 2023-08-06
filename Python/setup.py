from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'TACTINSA Serial Communication Protocol'
LONG_DESCRIPTION = 'A package that allows you to communicate betweeen Raspberry/Python and Arduino with the TACTINSA Serial Communication Protocol'

# Setting up
setup(
    name="tacticom",
    version=VERSION,
    author="DenisD3D",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
)
