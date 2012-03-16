"""
Setup and installation for the package.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="three",
    version="0.5.1",
    url="http://github.com/codeforamerica/three",
    author="Zach Williams",
    author_email="hey@zachwill.com",
    description="An easy-to-use wrapper for the Open311 API",
    packages=[
        'three'
    ],
    install_requires=[
        'mock',
        'relaxml',
        'requests',
        'simplejson',
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
