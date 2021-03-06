# -*- coding: utf-8 -*-
import os
import math

import pytest

from msl import loadlib
from msl.loadlib import IS_MAC
from msl.examples.loadlib import Cpp64, Fortran64, Echo64, DotNet64, FourPoints

c = None
f = None
d = None
n = None


def setup_module(module):
    global c, f, d, n
    if IS_MAC:  # the 32-bit server for Mac OS does not exist
        return
    c = Cpp64()
    f = Fortran64()
    d = Echo64(True)
    n = DotNet64()


def teardown_module(module):
    if IS_MAC:  # the 32-bit server for Mac OS does not exist
        return
    c.shutdown_server32()
    f.shutdown_server32()
    d.shutdown_server32()
    n.shutdown_server32()


@pytest.mark.skipif(IS_MAC, reason='the 32-bit server for Mac OS does not exist')
def test_unique_ports():
    for item in [f, d, n]:
        assert c.port != item.port
    for item in [d, n]:
        assert f.port != item.port
    assert d.port != n.port


@pytest.mark.skipif(IS_MAC, reason='the 32-bit server for Mac OS does not exist')
def test_lib_name():
    def get_name(path):
        return os.path.basename(path).split('.')[0]

    assert 'cpp_lib32' == get_name(c.lib32_path)
    assert 'fortran_lib32' == get_name(f.lib32_path)
    assert 'dotnet_lib32' == get_name(n.lib32_path)


@pytest.mark.skipif(IS_MAC, reason='the 32-bit server for Mac OS does not exist')
def test_server_version():
    assert loadlib.Server32.version().startswith('Python')


@pytest.mark.skipif(IS_MAC, reason='the 32-bit server for Mac OS does not exist')
def test_cpp():
    assert 3 == c.add(1, 2)
    assert -1002 == c.add(-1000, -2)
    assert 10.0 == pytest.approx(c.subtract(20.0, 10.0))
    assert -10.0 == pytest.approx(c.subtract(90.0, 100.0))
    assert 0.0 == pytest.approx(c.add_or_subtract(0.1234, -0.1234, True))
    assert 100.0 == pytest.approx(c.add_or_subtract(123.456, 23.456, False))

    a = 3.1415926
    values = [float(x) for x in range(100)]
    c_values = c.scalar_multiply(a, values)
    for i in range(len(values)):
        assert a*values[i] == pytest.approx(c_values[i])

    assert '0987654321' == c.reverse_string_v1('1234567890')
    assert '[abc x|z j 1 *&' == c.reverse_string_v2('&* 1 j z|x cba[')

    if loadlib.IS_PYTHON3:
        # can't pickle.dump a ctypes.Structure in Python 2 and then
        # pickle.load it in Python 3 (the interpreter that Server32 is running on)
        fp = FourPoints((0, 0), (0, 1), (1, 1), (1, 0))
        assert c.distance_4_points(fp) == 4.0

    assert c.circumference(0.5, 0) == 0.0
    assert c.circumference(0.5, 2) == 2.0
    assert c.circumference(0.5, 2**16) == pytest.approx(math.pi)
    assert c.circumference(1.0, 2**16) == pytest.approx(2.0*math.pi)


@pytest.mark.skipif(IS_MAC, reason='the 32-bit server for Mac OS does not exist')
def test_fortran():
    assert -127 == f.sum_8bit(-2**7, 1)
    assert 32766 == f.sum_16bit(2**15 - 1, -1)
    assert 123456789 == f.sum_32bit(123456788, 1)
    assert -9223372036854775807 == f.sum_64bit(-2**63, 1)
    assert -52487.570494 == pytest.approx(f.multiply_float32(40.874, -1284.131))
    assert 2.31e300 == pytest.approx(f.multiply_float64(1.1e100, 2.1e200))
    assert f.is_positive(1e-100)
    assert not f.is_positive(-1e-100)
    assert 3000 == f.add_or_subtract(1000, 2000, True)
    assert -1000 == f.add_or_subtract(1000, 2000, False)
    assert 1 == int(f.factorial(0))
    assert 1 == int(f.factorial(1))
    assert 120 == int(f.factorial(5))
    assert 2.73861278752583 == pytest.approx(f.standard_deviation([float(val) for val in range(1,10)]))
    assert 0.171650807137 == pytest.approx(f.besselJ0(8.0))
    assert '!dlrow olleh' == f.reverse_string('hello world!')

    a = [float(val) for val in range(1, 1000)]
    b = [3.0*val for val in range(1, 1000)]
    f_values = f.add_1D_arrays(a, b)
    for i in range(len(a)):
        assert a[i] + b[i] == pytest.approx(f_values[i])

    f_mat = f.matrix_multiply([[1., 2., 3.], [4., 5., 6.]], [[1., 2.], [3., 4.], [5., 6.]])
    assert 22.0 == pytest.approx(f_mat[0][0])
    assert 28.0 == pytest.approx(f_mat[0][1])
    assert 49.0 == pytest.approx(f_mat[1][0])
    assert 64.0 == pytest.approx(f_mat[1][1])


@pytest.mark.skipif(IS_MAC, reason='the 32-bit server for Mac OS does not exist')
def test_dummy():

    args, kwargs = d.send_data(True)
    assert args[0]
    assert {} == kwargs

    args, kwargs = d.send_data(x=1.0)
    assert args == ()
    assert kwargs == {'x': 1.0}

    x = [val for val in range(100)]
    y = range(9999)
    my_dict = {'x': x, 'y': y, 'text': 'abcd 1234 wxyz'}
    args, kwargs = d.send_data(111, 2.3, complex(-1.2, 2.30), (1, 2), x=x, y=y, my_dict=my_dict)
    assert args[0] == 111
    assert args[1] == 2.3
    assert args[2] == complex(-1.2, 2.30)
    assert args[3] == (1, 2)
    assert kwargs['x'] == x
    assert kwargs['y'] == y
    assert kwargs['my_dict'] == my_dict


@pytest.mark.skipif(IS_MAC, reason='the 32-bit server for Mac OS does not exist')
def test_dotnet():

    names = n.get_class_names()
    assert len(names) == 4
    assert 'StringManipulation' in names
    assert 'DotNetMSL.BasicMath' in names
    assert 'DotNetMSL.ArrayManipulation' in names
    assert 'StaticClass' in names

    assert 9 == n.add_integers(4, 5)
    assert 0.8 == pytest.approx(n.divide_floats(4., 5.))
    assert 458383.926 == pytest.approx(n.multiply_doubles(872.24, 525.525))
    assert 108.0 == pytest.approx(n.add_or_subtract(99., 9., True))
    assert 90.0 == pytest.approx(n.add_or_subtract(99., 9., False))

    a = 7.13141
    values = [float(x) for x in range(1000)]
    net_values = n.scalar_multiply(a, values)
    for i in range(len(values)):
        assert a*values[i] == pytest.approx(net_values[i])

    assert n.reverse_string('New Zealand') == 'dnalaeZ weN'

    net_mat = n.multiply_matrices([[1., 2., 3.], [4., 5., 6.]], [[1., 2.], [3., 4.], [5., 6.]])
    assert 22.0 == pytest.approx(net_mat[0][0])
    assert 28.0 == pytest.approx(net_mat[0][1])
    assert 49.0 == pytest.approx(net_mat[1][0])
    assert 64.0 == pytest.approx(net_mat[1][1])

    assert 33 == n.add_multiple(11, -22, 33, -44, 55)
    assert 'the experiment worked ' == n.concatenate('the ', 'experiment ', 'worked ', False, 'temporarily')
    assert 'the experiment worked temporarily' == n.concatenate('the ', 'experiment ', 'worked ', True, 'temporarily')


@pytest.mark.skipif(IS_MAC, reason='the 32-bit server for Mac OS does not exist')
def test_unicode_path():

    class Cpp64Encoding(loadlib.Client64):
        def __init__(self):
            super(Cpp64Encoding, self).__init__(
                module32='cpp32unicode',
                append_sys_path=os.path.dirname(__file__) + u'/uñicödé',
                append_environ_path=os.path.dirname(__file__) + u'/uñicödé',
            )

        def add(self, a, b):
            return self.request32('add', a, b)

    c2 = Cpp64Encoding()
    assert c2.add(-5, 3) == -2

    with pytest.raises(loadlib.Server32Error):
        c2.add('hello', 'world')

    try:
        c2.add('hello', 'world')
    except loadlib.Server32Error as e:
        print(e)  # must not raise an error

    c2.shutdown_server32()


@pytest.mark.skipif(IS_MAC, reason='the 32-bit server for Mac OS does not exist')
def test_server32_error():
    try:
        c.add('hello', 'world')
    except loadlib.Server32Error as e:
        assert e.name == 'TypeError'
        assert e.value.startswith('an integer is required')
        assert e.traceback.endswith('return self.lib.add(ctypes.c_int32(a), ctypes.c_int32(b))')
