"""Example demonstrating curvature adaptation in a geometry context."""
from acm.core import AdaptiveCurvatureMemory


def main() -> None:
    acm = AdaptiveCurvatureMemory(initial_curvature=2.0)
    for radius in [1, 2, 3]:
        curvature = 1 / radius
        acm.update(curvature)
        print(f"Radius {radius}: average curvature={acm.get_curvature():.4f}")


if __name__ == "__main__":
    main()
