import pytest
from acm.utils import moving_average


def test_moving_average():
    assert moving_average([1.0, 3.0, 5.0]) == pytest.approx(3.0)
