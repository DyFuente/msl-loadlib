import sys
from distutils.cmd import Command
from setuptools import setup, find_packages

from msl import loadlib


class ApiDocs(Command):
    """
    A custom command that calls sphinx-apidoc
    see: https://www.sphinx-doc.org/en/latest/man/sphinx-apidoc.html
    """
    description = 'builds the api documentation using sphinx-apidoc'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        command = [
            None,  # in Sphinx < 1.7.0 the first command-line argument was parsed, in 1.7.0 it became argv[1:]
            '--force',  # overwrite existing files
            '--module-first',  # put module documentation before submodule documentation
            '--separate',  # put documentation for each module on its own page
            '-o', './docs/_autosummary',  # where to save the output files
            'msl',  # the path to the Python package to document
        ]

        import sphinx
        if sphinx.version_info < (1, 7):
            from sphinx.apidoc import main
        else:
            from sphinx.ext.apidoc import main  # Sphinx also changed the location of apidoc.main
            command.pop(0)

        main(command)
        sys.exit(0)


class BuildDocs(Command):
    """
    A custom command that calls sphinx-build
    see: https://www.sphinx-doc.org/en/latest/man/sphinx-build.html
    """
    description = 'builds the documentation using sphinx-build'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sphinx

        command = [
            None,  # in Sphinx < 1.7.0 the first command-line argument was parsed, in 1.7.0 it became argv[1:]
            '-b', 'html',  # the builder to use, e.g., create a HTML version of the documentation
            '-a',  # generate output for all files
            '-E',  # ignore cached files, forces to re-read all source files from disk
            'docs',  # the source directory where the documentation files are located
            './docs/_build/html',  # where to save the output files
        ]

        if sphinx.version_info < (1, 7):
            from sphinx import build_main
        else:
            from sphinx.cmd.build import build_main  # Sphinx also changed the location of build_main
            command.pop(0)

        build_main(command)
        sys.exit(0)


def read(filename):
    with open(filename) as fp:
        text = fp.read()
    return text


# auto generate the MANIFEST.in file based on the platform
if 'sdist' not in sys.argv:
    with open('MANIFEST.in', 'w') as f:
        f.write('# This file is automatically generated. Do not modify.\n')
        f.write('recursive-include msl/examples/loadlib *.jar *.class\n')
        f.write('include msl/loadlib/py4j-wrapper.jar\n')
        f.write('include msl/examples/loadlib/dotnet_lib32.dll\n')
        f.write('include msl/examples/loadlib/dotnet_lib64.dll\n')
        f.write('recursive-include msl/loadlib {}*\n'.format(loadlib.SERVER_FILENAME))
        f.write('recursive-include msl/examples/loadlib *{}\n'.format(loadlib.DEFAULT_EXTENSION))
        if loadlib.IS_WINDOWS:
            f.write('include msl/loadlib/verpatch.exe\n')
else:
    with open('MANIFEST.in', 'w') as f:
        f.write('# This file is automatically generated. Do not modify.\n')
        f.write('recursive-include msl *.cpp *.h *.cs *.f90 *.java *.jar *.class *.so *.dll *.txt\n')
        f.write('include msl/loadlib/verpatch.exe\n')

testing = {'test', 'tests', 'pytest'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if testing else []

needs_sphinx = {'doc', 'docs', 'apidoc', 'apidocs', 'build_sphinx'}.intersection(sys.argv)
sphinx = ['sphinx', 'sphinx_rtd_theme'] if needs_sphinx else []

tests_require = ['pytest', 'pytest-cov', 'pythonnet', 'py4j']
if sys.version_info < (3, 4):
    tests_require += ['pathlib']
if loadlib.IS_WINDOWS:
    tests_require += ['comtypes']

setup(
    name='msl-loadlib',
    version=loadlib.__version__,
    author=loadlib.__author__,
    author_email='info@measurement.govt.nz',
    url='https://github.com/MSLNZ/msl-loadlib',
    description='Load a shared library (and access a 32-bit library from 64-bit Python)',
    long_description=read('README.rst'),
    license='MIT',
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
    ],
    setup_requires=sphinx + pytest_runner,
    tests_require=tests_require,
    install_requires=[],
    extras_require = {
        'clr': ['pythonnet'],
        'java': ['py4j'],
        'com': ['comtypes'],
        'all': ['pythonnet', 'py4j', 'comtypes'],
    },
    cmdclass={'docs': BuildDocs, 'apidocs': ApiDocs},
    packages=find_packages(include=('msl*',)),
    include_package_data=True,
)
