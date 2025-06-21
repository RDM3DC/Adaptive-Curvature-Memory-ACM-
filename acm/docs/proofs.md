# Proofs

This section collects short mathematical proofs for some of the algorithms and helper utilities used in ACM.

## Moving Average

For a finite sequence $x_1, \dots, x_n$, the helper `moving_average` returns
\[
\frac{1}{n}\sum_{i=1}^n x_i.
\]
This value always lies between the minimum and maximum of the inputs, by the standard bounds on an arithmetic mean.

## Curvature Update

`adjust_curvature(value, factor)` simply computes $value \times factor$ and is linear in both arguments. The `AdaptiveCurvatureMemory.get_curvature` method returns the average of stored curvatures, so it is bounded by the smallest and largest values currently in memory.

## Quantum Utilities

In `Interaction and entanglement demonstration.md` the CNOT matrix
\[
\begin{bmatrix}
1 & 0 & 0 & 0\\
0 & 1 & 0 & 0\\
0 & 0 & 0 & 1\\
0 & 0 & 1 & 0
\end{bmatrix}
\]
is unitary because $U^\dagger U = I$. The GHZ state built with amplitudes $1/\sqrt{2}$ is normalized because the sum of squared magnitudes equals 1.
