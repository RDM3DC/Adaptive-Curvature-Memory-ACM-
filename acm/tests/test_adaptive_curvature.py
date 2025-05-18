from acm.models import adjust_curvature


def test_adjust_curvature():
    assert adjust_curvature(2.0, 1.5) == 3.0
