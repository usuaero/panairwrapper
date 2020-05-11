"""panairwrapper: A wrapper for the Panair/A502 Fortran code."""

from setuptools import setup

setup(name='panairwrapper',
      version='0.0',
      description='A wrapper for the Panair/A502 Fortran code.',
      url='NA',
      author='usuaero',
      author_email='doug.hunsaker@usu.edu',
      license='MIT',
      packages=['panairwrapper'],
      install_requires=['numpy', 'scipy', 'PyQt5', 'pyqtgraph', 'PyOpenGL'],
      zip_safe=False)
