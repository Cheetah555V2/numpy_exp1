import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

N = 10000

points = np.random.uniform([-1,-1],[1,1],(N,2))

inside = points[:, 0]**2 + points[:, 1]**2 <= 1

count = np.sum(inside)

PI = 4 * count / N

print(f"PI is approximate to be {PI:.7f}")

# ---- plotting (small sample only) ----
sample_size = 2000
sample_points = points[:sample_size]
sample_inside = inside[:sample_size]

plt.figure(figsize=(6, 6))

# outside points
plt.scatter(
    sample_points[~sample_inside, 0],
    sample_points[~sample_inside, 1],
    s=5,
    label="Outside circle"
)

# inside points
plt.scatter(
    sample_points[sample_inside, 0],
    sample_points[sample_inside, 1],
    s=5,
    label="Inside circle"
)

# filled unit circle
circle = plt.Circle( # type: ignore
    (0, 0),
    1,
    alpha=0.25,
    color="orange",
    label="Unit circle"
)

plt.gca().add_patch(circle)

# formatting
plt.gca().set_aspect("equal", adjustable="box")
plt.xlabel("x")
plt.ylabel("y")
plt.title(f"π ≈ {PI:.7f}")
plt.legend(loc="upper right")

plt.show()