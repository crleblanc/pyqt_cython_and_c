from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = cythonize([
    Extension("pycproject.cprogram", ["pycproject/cprogram.pyx"],
              extra_objects=['libcproject.a'],
              include_dirs = ['include'],
              library_dirs = ['lib'])
    ])


setup(
  name = 'Python Cmake, Cython, PyQt demo',
  packages=['pycproject'],
  ext_modules = extensions,
)
