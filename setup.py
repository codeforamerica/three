"""
Setup and installation for the package.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="requests",
    version="0.1",
    author="Zach Williams",
    author_email="hey@zachwill.com",
    description="An easy-to-use wrapper for the Open311 API",
    long_description=open('README.md').read(),
    packages=[
        'three'
    ],
    install_requires=[
        'mock',
        'requests',
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
