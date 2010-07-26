import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(here, 'README.txt')).read()
__version__ = '0.5dev'
install_requires = [
    'pil',
    'aggdraw',
    ]

setup(
    name="cvs_mapping",
    version=__version__,
    description="A mapping application for rapidsms",
    keywords="django map",
    author="Mugisha Moses",
    author_email="mossplix@gmail.com",
    install_requires=install_requires,
    license='BSD',
    
    )
