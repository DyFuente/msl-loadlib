import os
import sys
import tempfile

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from msl.loadlib import ConnectionTimeoutError, IS_MAC

sys.path.append(os.path.join(os.path.dirname(__file__), 'bad_servers'))
from client import Client


def _raises(module32):
    path = os.path.join(tempfile.gettempdir(), 'msl-loadlib-stderr.txt')
    sys_stderr = sys.stderr  # keep a reference to the original object
    sys.stderr = open(path, 'w+')
    with pytest.raises(ConnectionTimeoutError):
        Client(module32)
    sys.stderr.seek(0)
    lines = sys.stderr.readlines()
    sys.stderr.close()
    os.remove(path)
    sys.stderr = sys_stderr
    return lines


@pytest.mark.skipif(IS_MAC, reason='the 32-bit server for Mac OS does not exist')
def test_no_server32_subclass():
    stderr_lines = _raises('no_server32_subclass')
    assert 'Module does not contain a class that is a subclass of Server32.' == stderr_lines[1].strip()


@pytest.mark.skipif(IS_MAC, reason='the 32-bit server for Mac OS does not exist')
def test_no_init():
    stderr_lines = _raises('no_init')
    assert 'class NoInit(Server32):' == stderr_lines[3].strip()


@pytest.mark.skipif(IS_MAC, reason='the 32-bit server for Mac OS does not exist')
def test_bad_init_args():
    stderr_lines = _raises('bad_init_args')
    assert 'class BadInitArgs(Server32):' == stderr_lines[3].strip()


@pytest.mark.skipif(IS_MAC, reason='the 32-bit server for Mac OS does not exist')
def test_no_super():
    stderr_lines = _raises('no_super')
    assert 'class NoSuper(Server32):' == stderr_lines[3].strip()


@pytest.mark.skipif(IS_MAC, reason='the 32-bit server for Mac OS does not exist')
def test_bad_super_init():
    stderr_lines = _raises('bad_super_init')
    assert 'class BadSuperInit(Server32):' == stderr_lines[3].strip()


@pytest.mark.skipif(IS_MAC, reason='the 32-bit server for Mac OS does not exist')
def test_bad_lib_path():
    stderr_lines = _raises('bad_lib_path')
    assert 'Cannot find the shared library' in stderr_lines[0]


@pytest.mark.skipif(IS_MAC, reason='the 32-bit server for Mac OS does not exist')
def test_bad_lib_type():
    stderr_lines = _raises('bad_lib_type')
    assert 'Cannot load libtype=invalid' in stderr_lines[0]


@pytest.mark.skipif(IS_MAC, reason='the 32-bit server for Mac OS does not exist')
def test_unexpected_error():
    stderr_lines = _raises('unexpected_error')
    assert 'ZeroDivisionError' in stderr_lines[0]


@pytest.mark.skipif(IS_MAC, reason='the 32-bit server for Mac OS does not exist')
def test_wrong_bitness():
    stderr_lines = _raises('wrong_bitness')
    assert 'Failed to load' in stderr_lines[0]
