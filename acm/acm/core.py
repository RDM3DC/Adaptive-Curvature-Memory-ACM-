"""Core module implementing the Adaptive Curvature Memory algorithm.

This module exposes the :class:`AdaptiveCurvatureMemory` class which keeps
a history of curvature values. The class provides methods to update the
stored values, retrieve the average curvature and reset the memory using
``reset``.
"""
from collections import deque
from typing import Deque, List


class AdaptiveCurvatureMemory:
    """Maintain a memory of curvature values and provide adaptive updates."""

    def __init__(self, initial_curvature: float = 1.0, memory_size: int = 10) -> None:
        self.memory_size = memory_size
        self.curvatures: Deque[float] = deque(maxlen=memory_size)
        self.curvatures.append(initial_curvature)

    def update(self, curvature: float) -> None:
        """Add a new curvature value to the memory."""
        self.curvatures.append(curvature)

    def get_curvature(self) -> float:
        """Return the average curvature from memory."""
        if not self.curvatures:
            return 0.0
        return sum(self.curvatures) / len(self.curvatures)

    def history(self) -> List[float]:
        """Return a list of stored curvature values."""
        return list(self.curvatures)

    def reset(self, initial_curvature: float = 1.0) -> None:
        """Clear stored curvatures and start with ``initial_curvature``.

        Parameters
        ----------
        initial_curvature:
            The curvature value to initialise the memory with after reset.
        """
        self.curvatures.clear()
        self.curvatures.append(initial_curvature)
