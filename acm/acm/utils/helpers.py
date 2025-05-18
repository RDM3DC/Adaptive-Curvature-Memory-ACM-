"""Helper utilities for ACM."""
from typing import Iterable, List


def moving_average(values: Iterable[float]) -> float:
    """Compute the arithmetic mean of the given values."""
    values_list: List[float] = list(values)
    if not values_list:
        return 0.0
    return sum(values_list) / len(values_list)
