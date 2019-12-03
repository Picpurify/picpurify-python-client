from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

requirements = [
    'requests>=2.13.0',
    ]

about = {}
with open(os.path.join(here, 'picpurify', 'version.py'), 'r') as f:
    exec(f.read(), about)

with open("README.md", "r") as fh:
    long_description = fh.read()   

setup(
    name="picpurify",
    version=about['__version__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.picpurify.com",
    license="MIT license",
    python_requires='>=2.7',
    packages=find_packages(),
    install_requires=requirements,
    author="Romain Cousseau",
    author_email="romain.cousseau@picpurify.com"      
)
