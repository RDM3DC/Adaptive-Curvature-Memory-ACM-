"""Example demonstrating curvature adaptation during optimization."""
from acm.core import AdaptiveCurvatureMemory
from acm.models import adjust_curvature


def main() -> None:
    acm = AdaptiveCurvatureMemory(initial_curvature=1.0, memory_size=5)
    for step in range(5):
        new_curvature = adjust_curvature(acm.get_curvature(), 1.1)
        acm.update(new_curvature)
        print(f"Step {step}: curvature={acm.get_curvature():.4f}")


if __name__ == "__main__":
    main()
