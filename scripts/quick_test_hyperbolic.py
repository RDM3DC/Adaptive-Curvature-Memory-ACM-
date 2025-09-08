from curve_memory.hyperbolic import pi_a_over_pi, adaptive_pi_metrics

print("Standard ratio:", pi_a_over_pi(1.0, 1.0))
print("Edge case zero curvature:", pi_a_over_pi(1.0, 0.0))

metrics = adaptive_pi_metrics(1.0, -1.0)
for key, val in metrics.items():
    print(f"{key}: {val}")
