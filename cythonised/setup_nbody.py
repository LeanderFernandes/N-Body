from distutils.core import setup
from Cython.Build import cythonize

setup(name='nbody_cython',
      est_modules=cythonize('./nbody_cython.pyx'))