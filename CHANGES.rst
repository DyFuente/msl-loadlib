=========
Changelog
=========

Version 0.7.0.dev0
==================

* Added

  - support for Python 3.8
  - compiled the C++ and FORTRAN examples for 64-bit macOS

* Changed

  - renamed ``utils.port_in_use()`` to ``utils.is_port_in_use()`` and added support for macOS

* Removed

  - Support for Python 3.4

Version 0.6.0 (2019.05.07)
==========================

* Added

  - a `shutdown_handler()` method to `Server32` (PR `#19 <https://github.com/MSLNZ/msl-loadlib/issues/19>`_)
  - a section to the docs that explains how to re-freeze the 32-bit server
  - a `kill_timeout` keyword argument to `Client64.shutdown_server32()`
  - the `rpc_timeout` keyword argument to `Client64` (thanks to @fake-name)
  - search `HKEY_CLASSES_ROOT\\Wow6432Node\\CLSID` in the Windows Registry for additional ActiveX `ProgID`'s
  - `extras_require` parameter to `setup.py` with keys: `clr`, `java`, `com`, `all`

* Changed

  - the frozen server32 executable (for Windows/Linux) now uses Python 3.7.3 and Python.NET 2.4.0
  - rename the optional `-asp` and `-aep` command line arguments to be `-s` and `-e` respectively
  - the current working directory where the 64-bit Python interpreter was executed from is now
    automatically appended to ``os.environ['PATH']`` on the 32-bit server
  - `freeze_server32.py` uses an `ArgumentParser` instead of directly reading from `sys.argv`

* Fixed

  - use ``sys.executable -m PyInstaller`` to create the 32-bit server
    (part of PR `#18 <https://github.com/MSLNZ/msl-loadlib/issues/18>`_)
  - the 32-bit server prints error messages to `sys.stderr` instead of `sys.stdout`
  - issue `#15 <https://github.com/MSLNZ/msl-loadlib/issues/15>`_ - wait for the
    subprocess that starts the 32-bit server to terminate and set a value for the `returncode`
  - issue `#14 <https://github.com/MSLNZ/msl-loadlib/issues/14>`_ - use `os.kill`
    to stop the 32-bit server if it won't stop after `kill_timeout` seconds

Version 0.5.0 (2019.01.06)
==========================

* Added

  - support for loading a Component Object Model (COM) library on Windows
  - the `requires_pythonnet` and `requires_comtypes` kwargs to ``freeze_server32.main()``
  - ``'clr'`` as an alias for ``'net'`` for the `libtype` parameter in `LoadLibrary`
  - the ``utils.get_com_info()`` function
  - support for unicode paths in Python 2
  - examples for working with numpy arrays and C++ structs

* Changed

  - the frozen server32 executable (for Windows/Linux) now runs on Python 3.6.8
  - if loading a .NET assembly succeeds but calling `GetTypes()` fails then a detailed error
    message is logged rather than raising the exception - the value of `lib` will be `None`
  - the default timeout value when waiting for the 32-bit server to start is now 10 seconds
  - the `Client64` class now raises `Server32Error` if the 32-bit server raises an exception
  - the `Client64` class now inherits from `object` and the reference to `HTTPConnection`
    is now a property value
  - the `__repr__` methods no longer include the id as a hex number

* Fixed

  - set ``sys.stdout = io.StringIO()`` if `quiet=True` on the server

Version 0.4.1 (2018.08.24)
==========================

* Added

  - the ``version_info`` namedtuple now includes a *releaselevel*
  - Support for Python 3.7

* Fixed

  - Issue `#11 <https://github.com/MSLNZ/msl-loadlib/issues/11>`_
  - ``utils.wait_for_server()`` raised `NameError: name 'TimeoutError' is not defined` for Python 2.7
  - ``utils.port_in_use()`` raised `UnicodeDecodeError` (`PR #9 <https://github.com/MSLNZ/msl-loadlib/pull/9>`_)
  - ``setup.py`` is now also compatible with Sphinx 1.7+

* Changed

  - the frozen server32 executable (for Windows/Linux) now runs on Python 3.6.6
  - pythonnet is now an optional dependency on Windows and py4j is now optional for all OS
  - rename `Dummy` example to `Echo`

* Removed

  - Support for Python 3.3

Version 0.4.0 (2018.02.28)
==========================

* Added

  - `Py4J <https://www.py4j.org/>`_ wrapper for loading ``.jar`` and ``.class`` Java files
  - example on how to load a library that was built with LabVIEW

* Fixed

  - Issue `#8 <https://github.com/MSLNZ/msl-loadlib/issues/8>`_
  - Issue `#7 <https://github.com/MSLNZ/msl-loadlib/issues/7>`_
  - ``AttributeError("'LoadLibrary' object has no attribute '_lib'") raised in repr()``

* Changed

  - rename ``DotNetContainer`` to ``DotNet``
  - use ``socket.socket.bind`` to select an available port instead of checking of
    calling ``utils.port_in_use``
  - moved the static methods to the ``msl.loadlib.utils`` module:
      + Client64.port_in_use -> utils.port_in_use
      + Client64.get_available_port -> utils.get_available_port
      + Client64.wait_for_server -> utils.wait_for_server
      + LoadLibrary.check_dot_net_config -> utils.check_dot_net_config
      + LoadLibrary.is_pythonnet_installed -> utils.is_pythonnet_installed

Version 0.3.2 (2017.10.18)
==========================

* Added

  - include ``os.environ['PATH']`` as a search path when loading a shared library
  - the frozen server32 executable (for Windows/Linux) now runs on Python 3.6.3
  - support that the package can now be installed by ``pip install msl-loadlib``

* Fixed

  - remove ``sys.getsitepackages()`` error for virtualenv (`issue #5 <https://github.com/MSLNZ/msl-loadlib/issues/5>`_)
  - received ``RecursionError`` when freezing freeze_server32.py with PyInstaller 3.3
  - replaced ``FileNotFoundError`` with ``IOError`` (for Python 2.7 support)
  - recompile cpp_lib\*.dll and fortran_lib\*.dll to not depend on external dependencies

Version 0.3.1 (2017.05.15)
==========================
- fix ReadTheDocs build error -- AttributeError: module 'site' has no attribute 'getsitepackages'
- strip whitespace from append_sys_path and append_environ_path
- make pythonnet a required dependency only for Windows

Version 0.3.0 (2017.05.09)
==========================
*NOTE: This release breaks backward compatibility*

- can now pass \*\*kwargs from the Client64 constructor to the Server32-subclass constructor
- new command line arguments for starting the 32-bit server: --kwargs, --append_environ_path
- renamed the --append_path command line argument to --append_sys_path
- Server32.interactive_console() works on Windows and Linux
- edit documentation (thanks to @karna48 for the pull request)

Version 0.2.3 (2017.04.11)
==========================
- the frozen server32 executable (for Windows/Linux) now uses Python v3.6.1 and Python.NET v2.3.0
- include ctypes.util.find_library and sys.path when searching for shared library

Version 0.2.2 (2017.03.03)
==========================
- refreeze server32 executables

Version 0.2.1 (2017.03.02)
==========================
- fix releaselevel bug

Version 0.2.0 (2017.03.02)
==========================
- examples now working in Linux
- fix MSL namespace
- include all C# modules, classes and System.Type objects in the .NET loaded-library object
- create a custom C# library for the examples
- edit docstrings and documentation
- many bug fixes

Version 0.1.0 (2017.02.15)
==========================
- Initial release
