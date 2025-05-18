import pytest
from acm.utils import moving_average


def test_moving_average_normal_list():
    values = [1.0, 2.0, 3.0, 4.0]
    assert moving_average(values) == pytest.approx(2.5)


def test_moving_average_empty_iterable():
    assert moving_average([]) == 0.0
