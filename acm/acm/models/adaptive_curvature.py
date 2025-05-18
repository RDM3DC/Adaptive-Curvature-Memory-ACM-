"""Curvature adjustment models."""


def adjust_curvature(value: float, factor: float) -> float:
    """Adjust curvature by a factor.

    Parameters
    ----------
    value: float
        Current curvature value.
    factor: float
        Multiplicative factor to adjust the curvature.

    Returns
    -------
    float
        Adjusted curvature value.
    """
    return value * factor
