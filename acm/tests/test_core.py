import pytest
from acm.core import AdaptiveCurvatureMemory


def test_memory_update_and_average():
    acm = AdaptiveCurvatureMemory(initial_curvature=2.0, memory_size=3)
    acm.update(4.0)
    acm.update(6.0)
    assert acm.get_curvature() == pytest.approx((2.0 + 4.0 + 6.0) / 3)


def test_memory_limit():
    acm = AdaptiveCurvatureMemory(initial_curvature=1.0, memory_size=2)
    acm.update(2.0)
    acm.update(3.0)
    # memory should only keep the last 2 values
    assert acm.history() == [2.0, 3.0]


def test_reset():
    acm = AdaptiveCurvatureMemory(initial_curvature=5.0, memory_size=3)
    acm.update(2.0)
    acm.reset()
    assert acm.history() == [5.0]
    assert acm.get_curvature() == 5.0
