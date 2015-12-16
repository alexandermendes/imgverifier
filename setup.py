# -*- coding: utf8 -*-

from setuptools import setup

try:
    readme = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
except:
    readme = ""
    
install_requirements = [
    "Pillow>=3.0.0",
    "scandir>=1.1"
]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    'pytest-cov>=2.2.0',
    'pytest>=2.8.4',
]

setup(
    name='imgverifier',
    version='1.1.0',
    author='Alexander Mendes',
    author_email='alexanderhmendes@gmail.com',
    description='Assists in preperation of BL digital assets for DLS ingest.',
    license="BSD",
    url='http://github.com/alexandermendes/imgverifier/',
    packages=['imgverifier'],
    long_description=readme,
    platforms="any",
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requirements,
    setup_requires=setup_requirements,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Topic :: Office/Business"
    ],
    tests_require=test_requirements,
    test_suite="tests",
)
